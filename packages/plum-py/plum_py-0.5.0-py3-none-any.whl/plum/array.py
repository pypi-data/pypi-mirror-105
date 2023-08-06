# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Array to bytes and bytes to array transform."""

from typing import Any, List, Optional, Sequence, Tuple, Type, Union

from .data import Data, DataMeta
from .dump import Record
from .transform import Transform

Dims = Sequence[Optional[int]]
Format = Union[Type[Data], Transform]

GREEDY_DIMS: Dims = (None,)


class ArrayX(Transform):

    """Array to bytes and bytes to array transform."""

    __dims__: Dims
    __df__: Tuple[Dims, Format]

    def __init__(self, name: str, fmt: Format, dims: Optional[Dims] = None) -> None:
        super().__init__(name)

        assert isinstance(fmt, (DataMeta, Transform))

        dims_tuple: Dims

        if dims is None:
            dims_tuple = GREEDY_DIMS
        else:
            dims_tuple = tuple(None if d is None else int(d) for d in dims)
            assert all(True if d is None else d > 0 for d in dims_tuple)

        nbytes: Optional[int] = fmt.__nbytes__

        if nbytes is not None:
            for dim in dims_tuple:
                if dim is None:
                    nbytes = None
                    break

                nbytes *= dim

        self.__df__ = dims_tuple, fmt
        self.__dims__ = dims_tuple
        self.__nbytes__ = nbytes

    @property
    def fmt(self) -> Format:
        """Array element format."""
        return self.__df__[1]

    @property
    def dims(self) -> Dims:
        """Array dimensions."""
        return self.__df__[0]

    def __unpack__(
        self,
        buffer: bytes,
        offset: int,
        dump: Optional[Record] = None,
        dims: Optional[Dims] = None,
    ) -> Tuple[List[Any], int]:
        # pylint: disable=arguments-differ
        if dump is not None:
            return self.__unpack_and_dump__(buffer, offset, dump, dims)

        x_dims, fmt = self.__df__

        if dims is None:
            dims = x_dims
            if None in dims[1:]:
                raise TypeError(
                    "array unpack does not support greedy dimension beyond first dimension"
                )

        array: List[Any] = []
        append = array.append

        this_dim, *item_dims = dims

        if this_dim is None:
            end = len(buffer)
            while offset < end:
                item, offset = fmt.__unpack__(buffer, offset, dump)
                append(item)

        elif item_dims:
            for _ in range(this_dim):
                item, offset = self.__unpack__(buffer, offset, dump, item_dims)
                append(item)
        else:
            for _ in range(this_dim):
                item, offset = fmt.__unpack__(buffer, offset, dump)
                append(item)

        return array, offset

    def __unpack_and_dump__(
        self,
        buffer: bytes,
        offset: int,
        dump: Record,
        dims: Optional[Dims] = None,
    ) -> Tuple[List[Any], int]:
        # pylint: disable=arguments-differ
        x_dims, fmt = self.__df__

        if dims is None:
            dims = x_dims
            if None in dims[1:]:
                raise TypeError(
                    "array unpack does not support greedy secondary dimensions"
                )

        array: List[Any] = []
        append = array.append

        this_dim, *item_dims = dims

        if this_dim is None:
            end = len(buffer)
            i = 0
            fmt_name = fmt.__name__
            while offset < end:
                item, offset = fmt.__unpack__(
                    buffer, offset, dump.add_record(access=f"[{i}]", fmt=fmt_name)
                )
                append(item)
                i += 1

        elif item_dims:
            for i in range(this_dim):
                item, offset = self.__unpack_and_dump__(
                    buffer, offset, dump.add_record(access=f"[{i}]"), item_dims
                )
                append(item)
        else:
            fmt_name = fmt.__name__
            for i in range(this_dim):
                item, offset = fmt.__unpack__(
                    buffer, offset, dump.add_record(access=f"[{i}]", fmt=fmt_name)
                )
                append(item)

        return array, offset

    def __pack__(
        self,
        value: List[Any],
        pieces: List[bytes],
        dump: Optional[Record] = None,
        dims: Optional[Dims] = None,
    ) -> None:
        # pylint: disable=arguments-differ
        if dump is not None:
            self.__pack_and_dump__(value, pieces, dump, dims)

        else:
            x_dims, fmt = self.__df__

            this_dim, *item_dims = x_dims if dims is None else dims

            try:
                actual_length = len(value)
            except TypeError:
                raise TypeError("invalid array value, retrying with dump") from None

            if this_dim is not None and actual_length != this_dim:
                raise TypeError("invalid array value, retrying with dump")

            if item_dims:
                for item in value:
                    self.__pack__(item, pieces, dump, item_dims)
            else:
                for item in value:
                    fmt.__pack__(item, pieces, dump)

    def __pack_and_dump__(
        self,
        value: List[Any],
        pieces: List[bytes],
        dump: Record,
        dims: Optional[Dims] = None,
    ) -> None:
        # pylint: disable=arguments-differ
        x_dims, fmt = self.__df__

        this_dim, *item_dims = x_dims if dims is None else dims

        try:
            actual_length = len(value)
        except TypeError:
            dump.value = value
            raise TypeError(
                f"invalid value, expected iterable of "
                f'{"any " if this_dim is None else ""}'
                f'length{"" if this_dim is None else " " + str(this_dim)}'
                f", got non-iterable"
            ) from None

        if this_dim is None:
            this_dim = actual_length

        if item_dims:
            for i, item in zip(range(this_dim), value):
                self.__pack_and_dump__(
                    item, pieces, dump.add_record(access=f"[{i}]"), item_dims
                )
        else:
            fmt_name = fmt.__name__

            for i, item in zip(range(this_dim), value):
                fmt.__pack__(
                    item, pieces, dump.add_record(access=f"[{i}]", fmt=fmt_name)
                )

        if actual_length != this_dim:
            for i in range(actual_length, this_dim):
                dump.add_record(access=f"[{i}]", value="<missing>")

            for i, item in zip(range(this_dim, actual_length), value[this_dim:]):
                dump.add_record(
                    access=f"[{i}] <extra>", value=item, separate=(i == this_dim)
                )
            raise TypeError(
                f"invalid value, expected iterable of "
                f"{this_dim} length, got iterable of length {actual_length}"
            )
