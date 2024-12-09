# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import io
from abc import ABC, abstractmethod


class Serializer[T](ABC):
    def deserialize(self, src: io.IOBase | bytes) -> T:
        if not isinstance(src, io.IOBase):
            src = io.BytesIO(src)

        return self._deserialize(src)

    @abstractmethod
    def _deserialize(self, src: io.IOBase) -> T: ...

    @abstractmethod
    def serialize(self, dst: io.IOBase, value: T) -> int: ...

    @abstractmethod
    def get_size(self) -> int: ...
