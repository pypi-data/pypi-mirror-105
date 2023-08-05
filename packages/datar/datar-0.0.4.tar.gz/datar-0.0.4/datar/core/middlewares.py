"""Middlewares for datar"""
import builtins

from typing import (
    Any, Callable, Iterable, List, Mapping, Optional, Tuple, Union
)
from abc import ABC

from pandas import DataFrame
from pandas.core.series import Series
from pipda.symbolic import DirectRefAttr
from pipda.context import ContextBase
from pipda.utils import DataEnv, functype

from .exceptions import ColumnNotExistingError
from .utils import (
    df_assign_item, expand_collections, sanitize_slice,
    vars_select, logger, to_df
)
from .types import DataFrameType

class Collection(list):
    """Mimic the c function in R

    All elements will be flattened

    Args:
        *args: The elements
    """
    def __init__(
            self, *args: Any,
            pool: Optional[Iterable[Any]] = None # used to evaluate slice
    ) -> None:
        super().__init__(expand_collections(args, pool=pool))

    def __neg__(self):
        return Negated(self)

    def __invert__(self):
        return Inverted(self)

class Inverted:
    """Inverted object, pending for next action"""

    def __init__(
            self,
            elems: Union[slice, str, list, tuple, Series]
    ) -> None:
        if isinstance(elems, slice):
            self.elems = elems
        else:
            self.elems = Collection(elems)

    def __repr__(self) -> str:
        return f"Inverted({self.elems})"

    def evaluate(
            self,
            all_columns: Iterable[Union[str, int]],
            raise_nonexists: bool = True
    ) -> List[int]:
        """Evaluate with current selected columns"""
        from ..base import setdiff

        out = []
        out_append = out.append
        if isinstance(self.elems, slice):
            out.extend(sanitize_slice(self.elems, all_columns, raise_nonexists))
        # Collection won't expand to Series
        # elif isinstance(self.elems, Series):
        #     out_append(all_columns.index(self.elems.name))
        else:
            all_columns_are_strs = all(
                isinstance(col, str) for col in all_columns
            )
            for elem in self.elems:
                if isinstance(elem, Series):
                    elem = elem.name
                if isinstance(elem, int) and all_columns_are_strs:
                    try:
                        elem = all_columns[elem]
                    except IndexError:
                        if raise_nonexists:
                            raise ColumnNotExistingError(
                                f"Column at location {elem} does not exist."
                            ) from None
                if elem not in all_columns and raise_nonexists:
                    raise ColumnNotExistingError(
                        f"Column `{elem}` does not exist."
                    )
                if elem not in all_columns:
                    out_append(elem)
                else:
                    out_append(all_columns.index(elem))

        return setdiff(range(len(all_columns)), out)


class Negated:
    """Negated object"""
    def __init__(self, elems: Union[slice, list]) -> None:
        """In case of -[1,2,3] or -c(1,2,3) or -f[1:3]"""
        self.elems = elems

    def __repr__(self) -> str:
        return f"Negated({self.elems})"

    def evaluate(
            self,
            all_columns: Optional[Iterable[Union[str, int]]] = None,
            raise_nonexists: bool = False
    ) -> List[int]:
        """Negate the elements"""
        elems = (
            reversed([
                i+1 for i in sanitize_slice(
                    self.elems,
                    all_columns,
                    raise_nonexists=raise_nonexists
                )
            ])
            if isinstance(self.elems, slice)
            else self.elems
        )
        return [-elem for elem in elems]

# class DescSeries(Series): # pylint: disable=too-many-ancestors
#     """Marking a series as descending"""
#     @property
#     def _constructor(self):
#         return DescSeries

class CurColumn:
    """Current column in across"""
    @classmethod
    def replace_args(cls, args: Tuple[Any], column: str) -> Tuple[Any]:
        """Replace self with the real column in args"""
        return tuple(column if isinstance(arg, cls) else arg for arg in args)

    @classmethod
    def replace_kwargs(
            cls,
            kwargs: Mapping[str, Any],
            column: str
    ) -> Mapping[str, Any]:
        """Replace self with the real column in kwargs"""
        return {
            key: column if isinstance(val, cls) else val
            for key, val in kwargs.items()
        }

class Across:
    """Across object"""
    def __init__(
            self,
            data: DataFrameType,
            cols: Optional[Iterable[str]] = None,
            fns: Optional[Union[
                Callable,
                Iterable[Callable],
                Mapping[str, Callable]
            ]] = None,
            names: Optional[str] = None,
            kwargs: Optional[Mapping[str, Any]] = None
    ) -> None:
        from ..dplyr.tidyselect import everything
        cols = everything(data) if cols is None else cols
        if not isinstance(cols, (list, tuple)):
            cols = [cols]
        cols = data.columns[vars_select(data.columns, *cols)]

        fns_list = []
        if callable(fns):
            fns_list.append({'fn': fns})
        elif isinstance(fns, (list, tuple)):
            fns_list.extend(
                {'fn': fn, '_fn': i, '_fn1': i+1}
                for i, fn in enumerate(fns)
            )
        elif isinstance(fns, dict):
            fns_list.extend(
                {'fn': value, '_fn': key}
                for key, value in fns.items()
            )
        elif fns is not None:
            raise ValueError(
                'Argument `_fns` of across must be None, a function, '
                'a formula, or a dict of functions.'
            )

        self.data = data
        self.cols = cols
        self.fns = fns_list
        self.names = names
        self.kwargs = kwargs or {}

    def evaluate(self, context: Optional[ContextBase] = None) -> DataFrame:
        """Evaluate object with context"""
        if not self.fns:
            self.fns = [{'fn': lambda x: x}]

        ret = None
        for column in self.cols:
            for fn_info in self.fns:
                render_data = fn_info.copy()
                render_data['_col'] = column
                fn = render_data.pop('fn')
                name_format = self.names
                if not name_format:
                    name_format = (
                        '{_col}_{_fn}' if '_fn' in render_data
                        else '{_col}'
                    )

                name = name_format.format(**render_data)
                if functype(fn) == 'plain':
                    value = fn(
                        self.data[column],
                        **CurColumn.replace_kwargs(self.kwargs, column)
                    )
                else:
                    # use fn's own context
                    value = fn(
                        DirectRefAttr(self.data, column),
                        **CurColumn.replace_kwargs(self.kwargs, column),
                        _env='piping'
                    )(self.data, context)

                # todo: check if it is proper
                #       group information lost
                if ret is None:
                    ret = to_df(value, name)
                else:
                    df_assign_item(ret, name, value)
        return DataFrame() if ret is None else ret

class IfCross(Across, ABC):
    """Base class for IfAny and IfAll"""
    if_type = None

    def evaluate(self, context: Optional[ContextBase] = None) -> DataFrame:
        """Evaluate the object with context"""
        agg_func = getattr(builtins, self.__class__.if_type)
        return super().evaluate(context).fillna(
            False
        ).astype(
            'boolean'
        ).apply(agg_func, axis=1)

class IfAny(IfCross):
    """For calls from dplyr's if_any"""
    if_type = 'any'

class IfAll(IfCross):
    """For calls from dplyr's if_all"""
    if_type = 'all'

class WithDataEnv:
    """Implements `with data` to mimic R's `with(data, ...)`"""
    def __init__(self, data: Any) -> None:
        self.data = DataEnv(data)

    def __enter__(self) -> Any:
        return self.data

    def __exit__(self, *exc_info) -> None:
        self.data.delete()

class Nesting:
    """Nesting objects for calls from tidyr.nesting"""
    def __init__(self, *columns: Any, **kwargs: Any) -> None:
        self.columns = []
        self.names = []

        id_prefix = hex(id(self))[2:6]
        for i, column in enumerate(columns):
            self.columns.append(column)
            if isinstance(column, str):
                self.names.append(column)
                continue
            try:
                # series
                name = column.name
            except AttributeError:
                name = f'_tmp{id_prefix}_{i}'
                logger.warning(
                    'Temporary name used for a nesting column, use '
                    'keyword argument instead to specify the key as name.'
                )
            self.names.append(name)

        for key, val in kwargs.items():
            self.columns.append(val)
            self.names.append(key)

    def __len__(self):
        return len(self.columns)
