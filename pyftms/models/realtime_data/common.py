# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import dataclasses as dc
import io
from typing import Any, cast, override

from ...serializer import BaseModel, get_serializer, model_meta


@dc.dataclass(frozen=True)
class RealtimeData(BaseModel):
    mask: dc.InitVar[int]

    @override
    @classmethod
    def _deserialize_asdict(cls, src: io.IOBase) -> dict[str, Any]:
        mask, kwargs = cast(int, get_serializer("u2").deserialize(src)), {}
        kwargs["mask"] = mask
        mask ^= 1

        for field, serializer in cls._iter_fields_serializers():
            if mask & 1:
                kwargs[field.name] = serializer.deserialize(src)

            mask >>= 1

            if not mask:
                break

        assert not src.read()

        return kwargs

    @override
    @classmethod
    def _calc_size(cls) -> int:
        return super()._calc_size() + 2


@dc.dataclass(frozen=True)
class RealtimeSpeedData(RealtimeData):
    speed_instant: float | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2.01",
        ),
    )
    """Instantaneous Speed"""

    speed_average: float | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2.01",
            features_bit=0,
        ),
    )
    """Average Speed"""


@dc.dataclass(frozen=True)
class StepRateData(BaseModel):
    step_rate_instant: int = dc.field(
        metadata=model_meta(
            format="u2",
        ),
    )
    """Step Rate Instant"""

    step_rate_average: int = dc.field(
        metadata=model_meta(
            format="u2",
        ),
    )
    """Step Rate Average"""


@dc.dataclass(frozen=True)
class ElevationGainData(BaseModel):
    elevation_gain_positive: int = dc.field(
        metadata=model_meta(
            format="u2",
        ),
    )
    """Elevation Gain Positive"""

    elevation_gain_negative: int = dc.field(
        metadata=model_meta(
            format="u2",
        ),
    )
    """Elevation Gain Negative"""


@dc.dataclass(frozen=True)
class InclinationData(BaseModel):
    inclination: float = dc.field(
        metadata=model_meta(
            format="s2.1",
        ),
    )
    """Inclination"""

    ramp_angle: float = dc.field(
        metadata=model_meta(
            format="s2.1",
        ),
    )
    """Ramp Angle"""


@dc.dataclass(frozen=True)
class EnergyData(BaseModel):
    energy_total: int = dc.field(
        metadata=model_meta(
            format="u2",
        ),
    )
    """Total Energy"""

    energy_per_hour: int = dc.field(
        metadata=model_meta(
            format="u2",
        ),
    )
    """Per Hour Energy"""

    energy_per_minute: int = dc.field(
        metadata=model_meta(
            format="u1",
        ),
    )
    """Per Minute Energy"""
