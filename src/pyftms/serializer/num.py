# Copyright 2024-2025, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import io
import re
from typing import override

from .serializer import Serializer

type FtmsNumbers = float | int | None


class NumSerializer(Serializer[FtmsNumbers]):
    """
    A simple class for reading/writing numbers from/to a stream.

    Stores the necessary parameters, including those for autoscaling during operations.
    """

    __slots__ = (
        "factor",
        "none",
        "sign",
        "size",
    )

    def __init__(self, format: str) -> None:
        """Initialize serializer.

        Parameters:
            format: Number format string.

        Raises:
            ValueError: If format string is wrong.
        """

        if (m := re.fullmatch(r"[us][1-4](\.\d{1,4})?", format)) is None:
            raise ValueError(f"Wrong serializer format: '{format}'.")

        self.factor = float(m.group(1) or "0")
        self.sign, self.size = format.startswith("s"), int(format[1])
        self.none = (1 << (8 * self.size - self.sign)) - 1

    @override
    def _deserialize(self, stream: io.IOBase) -> FtmsNumbers:
        """Deserialize number from stream.

        Deserialize number from stream, scaling it if necessary.

        Parameters:
            stream: IO stream.

        Returns:
            Readed value.

        Raises:
            EOFError: If the stream ends unexpectedly.
        """

        if len(data := stream.read(self.size)) != self.size:
            raise EOFError("Unexpected end of stream.")

        value = int.from_bytes(data, "little", signed=self.sign)

        if value == self.none:
            return

        if self.factor:
            value *= self.factor

        return value

    @override
    def serialize(self, stream: io.IOBase, value: FtmsNumbers) -> int:
        """Serialize number.

        Serialize number to a stream, pre-scaling if necessary.

        Parameters:
            stream: IO stream.
            value: Number to serialize.

        Returns:
            Number of written bytes.
        """

        if value is None:
            value = self.none

        elif self.factor:
            value /= self.factor

        data = int(value).to_bytes(self.size, "little", signed=self.sign)

        return stream.write(data)

    @override
    def get_size(self) -> int:
        return self.size
