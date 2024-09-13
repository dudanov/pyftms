# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import dataclasses as dc
from enum import STRICT, IntEnum, auto
from typing import cast

from ..serializer import ModelMeta
from .common import (
    BaseModel,
    CodeSwitchModel,
    IndoorBikeSimulationParameters,
    StopPauseCode,
    model_meta,
)
from .spin_down import SpinDownControlCode


class ControlCode(IntEnum, boundary=STRICT):
    """
    Control Op Codes.

    Described in section `4.16.1: Fitness Machine Control Point Procedure Requirements`.
    """

    REQUEST_CONTROL = 0x00
    """Request Control"""

    RESET = auto()
    """Reset"""

    SPEED = auto()
    """Set Target Speed"""

    INCLINE = auto()
    """Set Target Inclination"""

    RESISTANCE = auto()
    """Set Target Resistance Level"""

    POWER = auto()
    """Set Target Power"""

    HEART_RATE = auto()
    """Set Target Heart Rate"""

    START_RESUME = auto()
    """Start or Resume"""

    STOP_PAUSE = auto()
    """Stop or Pause"""

    ENERGY = auto()
    """Set Targeted Expended Energy"""

    STEPS_NUMBER = auto()
    """Set Targeted Number of Steps"""

    STRIDES_NUMBER = auto()
    """Set Targeted Number of Strides"""

    DISTANCE = auto()
    """Set Targeted Distance"""

    TIME_1 = auto()
    """Set Targeted Training Time"""

    TIME_2 = auto()
    """Set Targeted Time in Two Heart Rate Zones"""

    TIME_3 = auto()
    """Set Targeted Time in Three Heart Rate Zones"""

    TIME_5 = auto()
    """Set Targeted Time in Five Heart Rate Zones"""

    INDOOR_BIKE_SIMULATION = auto()
    """Set Indoor Bike Simulation Parameters"""

    WHEEL_CIRCUMFERENCE = auto()
    """Set Wheel Circumference"""

    SPIN_DOWN = auto()
    """Spin Down Control"""

    CADENCE = auto()
    """Set Targeted Cadence"""

    RESPONSE = 0x80
    """Response Code"""


class ResultCode(IntEnum, boundary=STRICT):
    """
    Result code of control operations.

    Described in section **4.16.2.22 Procedure Complete**.
    """

    SUCCESS = auto()
    """Success."""

    NOT_SUPPORTED = auto()
    """Operation Not Supported."""

    INVALID_PARAMETER = auto()
    """Invalid Parameter."""

    FAILED = auto()
    """Operation Failed."""

    NOT_PERMITTED = auto()
    """Control Not Permitted."""


@dc.dataclass(frozen=True)
class ControlIndicateModel(BaseModel):
    """
    Fitness Machine Control Point characteristic.

    Parameter Value Format of the Response Indication.

    Described in section `4.16.2.22 Procedure Complete`.
    """

    code: ControlCode = dc.field(
        metadata=model_meta(
            format="u1",
        )
    )
    """Response Code Op Code (0x80)"""

    request_code: ControlCode = dc.field(
        metadata=model_meta(
            format="u1",
        )
    )
    """Request Op Code"""

    result_code: ResultCode = dc.field(
        metadata=model_meta(
            format="u1",
        )
    )
    """Result Code"""


@dc.dataclass(frozen=True)
class ControlModel(CodeSwitchModel[ControlCode]):
    """
    Fitness Machine Control Point Characteristic Format.

    Described in section `4.16 Fitness Machine Control Point`.
    """

    VALID_TIME_LENGTH = (1, 2, 3, 5)

    target_speed: float | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2.01",
            features_bit=0,
            code=ControlCode.SPEED,
        ),
    )
    """Set Target Speed | Km/h"""

    target_inclination: float | None = dc.field(
        default=None,
        metadata=model_meta(
            format="s2.1",
            features_bit=1,
            code=ControlCode.INCLINE,
        ),
    )
    """Set Target Inclination | Percent"""

    target_resistance: float | None = dc.field(
        default=None,
        metadata=model_meta(
            format="s2.1",
            features_bit=2,
            code=ControlCode.RESISTANCE,
        ),
    )
    """Set Target Resistance Level | Unitless"""

    target_power: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="s2",
            features_bit=3,
            code=ControlCode.POWER,
        ),
    )
    """Set Target Power | Watt"""

    target_heart_rate: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u1",
            features_bit=4,
            code=ControlCode.HEART_RATE,
        ),
    )
    """Set Target Heart Rate | BPM"""

    stop_pause: StopPauseCode | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u1",
            features_bit=32,  # ignoring
            code=ControlCode.STOP_PAUSE,
        ),
    )
    """Stop or Pause | Enumeration"""

    target_energy: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2",
            features_bit=5,
            code=ControlCode.ENERGY,
        ),
    )
    """Set Targeted Expended Energy | Calorie"""

    target_steps: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2",
            features_bit=6,
            code=ControlCode.STEPS_NUMBER,
        ),
    )
    """Set Targeted Number of Steps | Step"""

    target_strides: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2",
            features_bit=7,
            code=ControlCode.STRIDES_NUMBER,
        ),
    )
    """Set Targeted Number of Strides | Stride"""

    target_distance: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u3",
            features_bit=8,
            code=ControlCode.DISTANCE,
        ),
    )
    """Set Targeted Distance | Meter"""

    target_time: tuple[int, ...] | None = dc.field(
        default=None,
    )
    """Set Targeted Training Time | Second"""

    target_time_1: tuple[int, ...] | None = dc.field(
        default=None,
        init=False,
        metadata=model_meta(
            format="u2",
            num=1,
            features_bit=9,
            code=ControlCode.TIME_1,
        ),
    )
    """Set Targeted Training Time | Second"""

    target_time_2: tuple[int, ...] | None = dc.field(
        default=None,
        init=False,
        metadata=model_meta(
            format="u2",
            num=2,
            features_bit=10,
            code=ControlCode.TIME_2,
        ),
    )
    """Set Targeted Time in Two Heart Rate Zones"""

    target_time_3: tuple[int, ...] | None = dc.field(
        default=None,
        init=False,
        metadata=model_meta(
            format="u2",
            num=3,
            features_bit=11,
            code=ControlCode.TIME_3,
        ),
    )
    """Set Targeted Time in Three Heart Rate Zones"""

    target_time_5: tuple[int, ...] | None = dc.field(
        default=None,
        init=False,
        metadata=model_meta(
            format="u2",
            num=5,
            features_bit=12,
            code=ControlCode.TIME_5,
        ),
    )
    """Set Targeted Time in Five Heart Rate Zones"""

    indoor_bike_simulation: IndoorBikeSimulationParameters | None = dc.field(
        default=None,
        metadata=model_meta(
            features_bit=13,
            code=ControlCode.INDOOR_BIKE_SIMULATION,
        ),
    )
    """Set Indoor Bike Simulation Parameters"""

    wheel_circumference: float | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2.1",
            features_bit=14,
            code=ControlCode.WHEEL_CIRCUMFERENCE,
        ),
    )
    """Set Wheel Circumference"""

    spin_down: SpinDownControlCode | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u1",
            features_bit=15,
            code=ControlCode.SPIN_DOWN,
        ),
    )
    """Spin Down Control | Enumeration"""

    target_cadence: float | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2.5",
            features_bit=16,
            code=ControlCode.CADENCE,
        ),
    )
    """Set Targeted Cadence | 1/minute"""

    def __post_init__(self):
        if self.code is not None:
            return

        # here only after manual initialization without 'code'.

        if (value := self.target_time) is not None:
            if (sz := len(value)) not in self.VALID_TIME_LENGTH:
                raise ValueError(
                    f"Valid number of 'target_time' values are: {self.VALID_TIME_LENGTH}"
                )

            object.__setattr__(self, f"target_time_{sz}", value)
            object.__setattr__(self, "target_time", None)

        # find command code by field
        for field in dc.fields(self):
            if (value := getattr(self, field.name)) is None:
                continue

            if meta := cast(ModelMeta, field.metadata):
                return object.__setattr__(self, "code", meta.get("code"))

        raise ValueError("Code not found.")
