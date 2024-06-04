# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import io
import re
from typing import override

from .serializer import Serializer

SupportedNumbers = int | float | None

_PARAM_PATTERN = re.compile(r"[us][1-8](\.\d{1,8})?$")


def _parse_fmt(fmt: str) -> tuple[int, float | None, bool]:
    if m := _PARAM_PATTERN.match(fmt):
        x = m.group(1)

        return int(fmt[1]), None if x is None else float(x), fmt[0] == "s"

    raise ValueError("Wrong serializer format.")


class NumSerializer(Serializer[SupportedNumbers]):
    """
    A simple class for reading/writing numbers from/to a stream.

    Stores the necessary parameters, including those for autoscaling during operations.
    """

    __slots__ = "size", "factor", "sign"

    def __init__(self, format: str) -> None:
        self.size, self.factor, self.sign = _parse_fmt(format)

    def _none(self) -> int:
        """Calculate FTMS `Data Not Available` value."""

        return (1 << (8 * self.size - self.sign)) - 1

    @override
    def _deserialize(self, src: io.IOBase) -> SupportedNumbers:
        """
        Reads a number from a stream, scaling it if necessary.

        Raise an `EOFError` exception if the stream ends unexpectedly.

        Parameters:
            reader: IOBase - I/O reader.
        Returns:
            SupportedValueTypes - readed value.
        """
        data = src.read(self.size)

        if len(data) != self.size:
            raise EOFError("Unexpected end of stream.")

        value = int.from_bytes(data, "little", signed=self.sign)

        if value == self._none():
            value = None

        elif self.factor:
            value *= self.factor

        return value

    @override
    def serialize(self, dst: io.IOBase, value: SupportedNumbers) -> int:
        """
        Writes a number to a stream, pre-scaling if necessary.

        Parameters:
            writer: IOBase - I/O writer.
            value: SupportedValueTypes - value to write.
        Returns:
            int - number of written bytes.
        """
        if value is None:
            value = self._none()

        elif self.factor:
            value /= self.factor

        b = int(value).to_bytes(self.size, "little", signed=self.sign)

        return dst.write(b)

    @override
    def get_size(self) -> int:
        return self.size
