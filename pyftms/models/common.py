# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import dataclasses as dc
import io
from enum import STRICT, IntEnum, auto
from typing import Any, Generic, TypeVar, cast, override

from ..serializer import BaseModel, ModelMeta, model_meta


class StopPauseCode(IntEnum, boundary=STRICT):
    """
    Code of `Stop or Pause` control and status messages.

    Described in section `4.16.2.9: Stop or Pause Procedure`.
    """

    STOP = auto()
    """Stop."""
    PAUSE = auto()
    """Pause."""


@dc.dataclass(frozen=True)
class IndoorBikeSimulationParameters(BaseModel):
    """
    Indoor Bike Simulation Parameters

    Described in section **4.16.2.18: Set Indoor Bike Simulation Parameters Procedure**.
    """

    wind_speed: float = dc.field(
        metadata=model_meta(
            format="s2.001",
        )
    )
    """
    Wind Speed.
    
    Units: `meters per second (mps)`.
    """

    grade: float = dc.field(
        metadata=model_meta(
            format="s2.01",
        )
    )
    """
    Grade.
    
    Units: `%`.
    """

    rolling_resistance: float = dc.field(
        metadata=model_meta(
            format="u1.0001",
        )
    )
    """
    Coefficient of Rolling Resistance.
    
    Units: `unitless`.
    """

    wind_resistance: float = dc.field(
        metadata=model_meta(
            format="u1.01",
        )
    )
    """
    Wind Resistance Coefficient.
    
    Units: `kilogram per meter (kg/m)`.
    """


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
    def _deserialize_asdict(cls, src: io.IOBase) -> dict[str, Any]:
        kwargs, it = {}, cls._iter_fields_serializers()
        code = cast(int, next(it)[1].deserialize(src))
        kwargs["code"] = code

        for field, serializer in it:
            meta = cast(ModelMeta, field.metadata)

            if meta.get("code") != code:
                continue

            name, value = field.name, serializer.deserialize(src)

            # remove digit suffix of 'target_time_x' property
            if name[-1].isdecimal():
                name = name[:-2]

            kwargs[name] = value

            break

        assert not src.read()

        return kwargs
