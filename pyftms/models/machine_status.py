# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import dataclasses as dc
from enum import STRICT, IntEnum, auto

from .common import (
    CodeSwitchModel,
    IndoorBikeSimulationParameters,
    StopPauseCode,
    model_meta,
)
from .spin_down import SpinDownStatusCode


class MachineStatusCode(IntEnum, boundary=STRICT):
    """
    Fitness Machine Status.

    Described in section **4.16.1: Fitness Machine Control Point Procedure Requirements**.
    """

    RESET = auto()
    """Reset"""

    STOP_PAUSE = auto()
    """Fitness Machine Stopped or Paused by the User"""

    STOP_SAFETY = auto()
    """Fitness Machine Stopped by Safety Key"""

    START_RESUME = auto()
    """Fitness Machine Started or Resumed by the User"""

    SPEED = auto()
    """Target Speed Changed"""

    INCLINE = auto()
    """Target Incline Changed"""

    RESISTANCE = auto()
    """Target Resistance Level Changed"""

    POWER = auto()
    """Target Power Changed"""

    HEART_RATE = auto()
    """Target Heart Rate Changed"""

    ENERGY = auto()
    """Targeted Expended Energy Changed"""

    STEPS_NUMBER = auto()
    """Targeted Number of Steps Changed"""

    STRIDES_NUMBER = auto()
    """Targeted Number of Strides Changed"""

    DISTANCE = auto()
    """Targeted Distance Changed"""

    TIME_1 = auto()
    """Targeted Training Time Changed"""

    TIME_2 = auto()
    """Targeted Time in Two Heart Rate Zones Changed"""

    TIME_3 = auto()
    """Targeted Time in Three Heart Rate Zones Changed"""

    TIME_5 = auto()
    """Targeted Time in Five Heart Rate Zones Changed"""

    INDOOR_BIKE_SIMULATION = auto()
    """Indoor Bike Simulation Parameters Changed"""

    WHEEL_CIRCUMFERENCE = auto()
    """Wheel Circumference Changed"""

    SPIN_DOWN = auto()
    """Spin Down Status"""

    CADENCE = auto()
    """Targeted Cadence Changed"""

    LOST_CONTROL = 0xFF
    """Control Permission Lost"""


@dc.dataclass(frozen=True)
class MachineStatusModel(CodeSwitchModel[MachineStatusCode]):
    """
    Structure of the Fitness Machine Status characteristic.

    Described in section **4.17 Fitness Machine Status**.
    """

    stop_pause: StopPauseCode | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u1",
            code=MachineStatusCode.STOP_PAUSE,
        ),
    )
    """Stopped or Paused Event | Enumeration"""

    target_speed: float | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2.01",
            code=MachineStatusCode.SPEED,
        ),
    )
    """New Target Speed | Km/h"""

    target_inclination: float | None = dc.field(
        default=None,
        metadata=model_meta(
            format="s2.1",
            code=MachineStatusCode.INCLINE,
        ),
    )
    """New Target Inclination | Percent"""

    target_resistance: float | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u1.1",
            code=MachineStatusCode.RESISTANCE,
        ),
    )
    """New Target Resistance Level | Unitless"""

    target_power: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="s2",
            code=MachineStatusCode.POWER,
        ),
    )
    """New Target Power | Watt"""

    target_heart_rate: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u1",
            code=MachineStatusCode.HEART_RATE,
        ),
    )
    """New Target Heart Rate | BPM"""

    target_energy: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2",
            code=MachineStatusCode.ENERGY,
        ),
    )
    """New Targeted Expended Energy | Calorie"""

    target_steps: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2",
            code=MachineStatusCode.STEPS_NUMBER,
        ),
    )
    """New Targeted Number of Steps | Step"""

    target_strides: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2",
            code=MachineStatusCode.STRIDES_NUMBER,
        ),
    )
    """New Targeted Number of Strides | Stride"""

    target_distance: int | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u3",
            code=MachineStatusCode.DISTANCE,
        ),
    )
    """New Targeted Distance | Meter"""

    target_time_1: tuple[int, ...] | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2",
            num=1,
            code=MachineStatusCode.TIME_1,
        ),
    )
    """New Targeted Training Time | Second"""

    target_time_2: tuple[int, ...] | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2",
            num=2,
            code=MachineStatusCode.TIME_2,
        ),
    )
    """New Targeted Time in Two Heart Rate Zones"""

    target_time_3: tuple[int, ...] | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2",
            num=3,
            code=MachineStatusCode.TIME_3,
        ),
    )
    """New Targeted Time in Three Heart Rate Zones"""

    target_time_5: tuple[int, ...] | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2",
            num=5,
            code=MachineStatusCode.TIME_5,
        ),
    )
    """New Targeted Time in Five Heart Rate Zones"""

    indoor_bike_simulation: IndoorBikeSimulationParameters | None = dc.field(
        default=None,
        metadata=model_meta(
            code=MachineStatusCode.INDOOR_BIKE_SIMULATION,
        ),
    )
    """New Indoor Bike Simulation Parameters"""

    wheel_circumference: float | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2.1",
            code=MachineStatusCode.WHEEL_CIRCUMFERENCE,
        ),
    )
    """New Wheel Circumference"""

    spin_down_status: SpinDownStatusCode | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u1",
            code=MachineStatusCode.SPIN_DOWN,
        ),
    )
    """Spin Down Control | Enumeration"""

    target_cadence: float | None = dc.field(
        default=None,
        metadata=model_meta(
            format="u2.5",
            code=MachineStatusCode.CADENCE,
        ),
    )
    """New Targeted Cadence | 1/minute"""
