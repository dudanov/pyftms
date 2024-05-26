# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import dataclasses as dc
import io
import itertools
from enum import STRICT, IntEnum, auto
from typing import Any, Generic, TypeVar, cast, override

from ..serializer import BaseModel, ModelMeta, get_serializer, model_meta


class StopPauseCode(IntEnum, boundary=STRICT):
    """
    Code of `Stop or Pause` control and status messages.

    Described in section `4.16.2.9: Stop or Pause Procedure`.
    """

    STOP = auto()
    """Stop"""
    PAUSE = auto()
    """Pause"""


@dc.dataclass(frozen=True)
class IndoorBikeSimulationParameters(BaseModel):
    """
    Indoor Bike Simulation Parameters

    Described in section `4.16.2.18: Set Indoor Bike Simulation Parameters Procedure`.

    Fields:
        - `Wind Speed` | Meters Per Second (mps)
        - `Grade` | Percentage
        - `Coefficient of Rolling Resistance` | Unitless
        - `Wind Resistance Coefficient` | Kilogram per Meter (Kg/m)
    """

    wind_speed: float = dc.field(
        metadata=model_meta(
            format="s2.001",
        )
    )

    grade: float = dc.field(
        metadata=model_meta(
            format="s2.01",
        )
    )

    rolling_resistance: float = dc.field(
        metadata=model_meta(
            format="u1.0001",
        )
    )

    wind_resistance: float = dc.field(
        metadata=model_meta(
            format="u1.01",
        )
    )


T = TypeVar("T", bound=int)


@dc.dataclass(frozen=True)
class CodeSwitchModel(Generic[T], BaseModel):
    """Base model based on a code attribute and associated parameter attributes."""

    code: T | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u1",
        ),
    )
    """Code | Enumeration"""

    @override
    @classmethod
    def _deserialize_dict(cls, src: io.IOBase) -> dict[str, Any]:
        code, kwargs = cast(int, get_serializer("u1").deserialize(src)), {}
        kwargs["code"] = code

        for k, s in itertools.islice(cls._iter_fields_serializers(), 1, None):
            meta = cast(ModelMeta, k.metadata)

            if meta["code"] != code:
                continue

            name, value = k.name, s.deserialize(src)

            # remove digit suffix of 'target_time_x' property
            if name[-1].isdecimal():
                name = name[:-2]

            kwargs[name] = value

            break

        assert not src.read()

        return kwargs
