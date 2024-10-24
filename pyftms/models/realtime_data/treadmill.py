# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import dataclasses as dc

from .common import (
    BaseModel,
    EnergyData,
    InclinationData,
    RealtimeSpeedData,
    model_meta,
)


@dc.dataclass(frozen=True)
class ElevationGainData(BaseModel):
    elevation_gain_positive: int = dc.field(
        metadata=model_meta(
            format="u2.1",
        ),
    )
    """Elevation Gain Positive"""

    elevation_gain_negative: int = dc.field(
        metadata=model_meta(
            format="u2.1",
        ),
    )
    """Elevation Gain Negative"""


@dc.dataclass(frozen=True)
class ForceOnBeltData(BaseModel):
    force_on_belt: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="s2",
        ),
    )
    """Force On Belt"""

    power_output: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="s2",
        ),
    )
    """Output Power"""


@dc.dataclass(frozen=True)
class TreadmillData(RealtimeSpeedData):
    distance_total: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u3",
            features_bit=2,
        ),
    )
    """Total Distance"""

    inclination: InclinationData | None = dc.field(
        default=None,
        metadata=model_meta(
            features_bit=3,
        ),
    )
    """Inclination and Ramp Angle Data"""

    elevation_gain: ElevationGainData | None = dc.field(
        default=None,
        metadata=model_meta(
            features_bit=4,
        ),
    )
    """Elevation Gain Data"""

    pace_instant: float | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u1.1",
            features_bit=5,
        ),
    )
    """Instantaneous Speed"""

    pace_average: float | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u1.1",
            features_bit=5,
        ),
    )
    """Average Speed"""

    energy: EnergyData | None = dc.field(
        default=None,
        metadata=model_meta(
            features_bit=9,
        ),
    )
    """Energy Data"""

    heart_rate: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u1",
            features_bit=10,
        ),
    )
    """Heart Rate"""

    metabolic_equivalent: float | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u1.1",
            features_bit=11,
        ),
    )
    """Metabolic Equivalent"""

    time_elapsed: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2",
            features_bit=12,
        ),
    )
    """Elapsed Time"""

    time_remaining: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2",
            features_bit=13,
        ),
    )
    """Remaining Time"""

    force_on_belt: ForceOnBeltData | None = dc.field(
        default=None,
        metadata=model_meta(
            features_bit=15,
        ),
    )
    """Force On Belt and Power Output"""

    step_count: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u3",
            features_bit=6,
        ),
    )
    """Steps Count"""
