# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import dataclasses as dc

from .common import EnergyData, RealtimeSpeedData, model_meta


@dc.dataclass(frozen=True)
class IndoorBikeData(RealtimeSpeedData):
    cadence_instant: float | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2.5",
            features_bit=1,
        ),
    )
    """Instantaneous Cadence"""

    cadence_average: float | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2.5",
            features_bit=1,
        ),
    )
    """Average Cadence"""

    distance_total: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u3",
            features_bit=2,
        ),
    )
    """Total Distance"""

    resistance_level: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="s2",
            features_bit=7,
        ),
    )
    """Resistance Level"""

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
