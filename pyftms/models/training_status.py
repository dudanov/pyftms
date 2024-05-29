# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import dataclasses as dc
from enum import STRICT, IntEnum, IntFlag, auto

from .common import BaseModel, model_meta


class TrainingStatusFlags(IntFlag, boundary=STRICT):
    """
    Training Status.

    Represents the current training state while a user is exercising.

    Described in section **4.10.1.2: Training Status Field**.
    """

    STRING_PRESENT = auto()
    """Other."""

    EXTENDED_STRING = auto()
    """Idle."""


class TrainingStatusCode(IntEnum, boundary=STRICT):
    """
    Training Status.

    Represents the current training state while a user is exercising.

    Described in section **4.10.1.2: Training Status Field**.
    """

    OTHER = 0
    """Other."""

    IDLE = auto()
    """Idle."""

    WARMING_UP = auto()
    """Warming Up."""

    LOW_INTENSITY_INTERVAL = auto()
    """Low Intensity Interval."""

    HIGH_INTENSITY_INTERVAL = auto()
    """High Intensity Interval."""

    RECOVERY_INTERVAL = auto()
    """Recovery Interval."""

    ISOMETRIC = auto()
    """Isometric."""

    HEART_RATE_CONTROL = auto()
    """Heart Rate Control."""

    FITNESS_TEST = auto()
    """Fitness Test."""

    SPEED_TOO_LOW = auto()
    """Speed Outside of Control Region - Low (increase speed to return to controllable region)."""

    SPEED_TOO_HIGH = auto()
    """Speed Outside of Control Region - High (decrease speed to return to controllable region)."""

    COOL_DOWN = auto()
    """Cool Down."""

    WATT_CONTROL = auto()
    """Watt Control."""

    MANUAL_MODE = auto()
    """Manual Mode (Quick Start)."""

    PRE_WORKOUT = auto()
    """Pre-Workout."""

    POST_WORKOUT = auto()
    """Post-Workout."""


@dc.dataclass(frozen=True)
class TrainingStatusModel(BaseModel):
    """
    Structure of the Training Status Characteristic.

    Described in section **4.10 Training Status**.
    """

    flags: TrainingStatusFlags = dc.field(
        metadata=model_meta(
            format="u1",
        )
    )
    """Flags Field."""

    code: TrainingStatusCode = dc.field(
        metadata=model_meta(
            format="u1",
        )
    )
    """Training Status Field."""
