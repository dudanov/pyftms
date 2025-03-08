# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import dataclasses as dc

from .common import BaseModel, EnergyData, RealtimeData, model_meta


@dc.dataclass(frozen=True)
class StrokeRateData(BaseModel):
    stroke_rate_instant: float = dc.field(
        metadata=model_meta(
            format="u1.5",
        ),
    )
    """Stroke Rate"""

    stroke_count: int = dc.field(
        metadata=model_meta(
            format="u2",
        ),
    )
    """Stroke Count"""


@dc.dataclass(frozen=True)
class RowerData(RealtimeData):
    stroke_rate: StrokeRateData | None = dc.field(
        default=None,
        metadata=model_meta(),
    )
    """Stroke Rate Data"""

    stroke_rate_average: float | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u1.5",
            features_bit=1,
        ),
    )
    """Average Stroke Rate"""

    distance_total: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u3",
            features_bit=2,
        ),
    )
    """Total Distance"""

    split_time_instant: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2",
            features_bit=5,
        ),
    )
    """Instantaneous Split Time"""

    split_time_average: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2",
            features_bit=5,
        ),
    )
    """Average Split Time"""

    power_instant: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="s2",
            features_bit=14,
        ),
    )
    """Instantaneous Power"""

    power_average: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="s2",
            features_bit=14,
        ),
    )
    """Average Power"""

    resistance_level: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="s2",
            features_bit=7,
        ),
    )
    """Resistance Level"""

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
