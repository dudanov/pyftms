# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

from typing import Callable, Literal, NamedTuple, NotRequired, TypedDict

from ...models import (
    IndoorBikeSimulationParameters,
    SpinDownControlCode,
    SpinDownSpeedData,
    SpinDownStatusCode,
    TrainingStatusCode,
)
from ..properties import MovementDirection

FtmsNumbers = int | float
ControlSource = Literal["callback", "user", "safety", "other"]
SimpleControlEvents = Literal["start", "stop", "pause", "reset"]


class SpinDownEventData(TypedDict, total=False):
    target_speed: SpinDownSpeedData
    """From fitness machine to client. Indicate successfully operation."""
    code: SpinDownControlCode
    """From client to fitness machine. START or IGNORE."""
    status: SpinDownStatusCode
    """From fitness machine to client."""


class SetupEventData(TypedDict, total=False):
    """`SetupEvent` data."""

    indoor_bike_simulation: IndoorBikeSimulationParameters
    """Indoor Bike Simulation Parameters."""
    target_cadence: float
    target_distance: int
    target_energy: int
    """efqrefwerf"""
    target_heart_rate: int
    target_inclination: float
    target_power: int
    target_resistance: float
    target_speed: float
    target_steps: int
    target_strides: int
    target_time: tuple[int, ...]
    wheel_circumference: float


class UpdateEventData(TypedDict, total=False):
    cadence_average: float
    cadence_instant: float
    distance_total: int
    elevation_gain_negative: int
    elevation_gain_positive: int
    energy_per_hour: int
    energy_per_minute: int
    energy_total: int
    force_on_belt: int
    heart_rate: int
    inclination: float
    metabolic_equivalent: float
    movement_direction: MovementDirection
    pace_average: int | float
    pace_instant: int | float
    power_average: int
    power_instant: int
    power_output: int
    ramp_angle: float
    resistance_level: int | float
    speed_average: float
    speed_instant: float
    step_rate_average: int
    step_rate_instant: int
    stride_count: int
    stroke_count: int
    stroke_rate_average: float
    stroke_rate_instant: float
    time_elapsed: int
    time_remaining: int


class TrainingStatusEventData(TypedDict):
    code: TrainingStatusCode
    string: NotRequired[str]


class TrainingStatusEvent(NamedTuple):
    """Training Status Event"""

    event_id: Literal["training_status"]
    event_data: TrainingStatusEventData


class UpdateEvent(NamedTuple):
    """Update event"""

    event_id: Literal["update"]
    event_data: UpdateEventData


class SpinDownEvent(NamedTuple):
    """Spin Down Procedure Event"""

    event_id: Literal["spin_down"]
    event_data: SpinDownEventData


class SetupEvent(NamedTuple):
    """Setting up parameter event"""

    event_id: Literal["setup"]
    event_data: SetupEventData
    event_source: ControlSource


class ControlEvent(NamedTuple):
    """Simple Control Event"""

    event_id: SimpleControlEvents
    event_source: ControlSource


FtmsEvents = (
    UpdateEvent | SetupEvent | ControlEvent | TrainingStatusEvent | SpinDownEvent
)
"""Tagged union of FTMS events."""

FtmsCallback = Callable[[FtmsEvents], None]
"""Callback function to receive FTMS events."""
