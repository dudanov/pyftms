# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import io
from typing import Generic, Iterator, override

from .serializer import Serializer, T


class ListSerializer(Generic[T], Serializer[Iterator[T]]):
    def __init__(self, serializer: Serializer[T], n: int) -> None:
        assert n > 0
        self._serializer = serializer
        self._len = n

    @override
    def serialize(self, dst: io.IOBase, value: Iterator[T]) -> int:
        return sum(self._serializer.serialize(dst, x) for x in value)

    @override
    def _deserialize(self, src: io.IOBase) -> Iterator[T]:
        return (self._serializer._deserialize(src) for _ in range(self._len))

    @override
    def get_size(self) -> int:
        return self._serializer.get_size() * self._len
