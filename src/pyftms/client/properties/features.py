# Copyright 2024-2025, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import io
import logging
from enum import STRICT, IntEnum, IntFlag, auto
from types import MappingProxyType
from typing import NamedTuple

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

from ...serializer import NumSerializer
from ..const import (
    FEATURE_UUID,
    HEART_RATE_RANGE_UUID,
    INCLINATION_RANGE_UUID,
    POWER_RANGE_UUID,
    RESISTANCE_LEVEL_RANGE_UUID,
    SPEED_RANGE_UUID,
    TARGET_HEART_RATE,
    TARGET_INCLINATION,
    TARGET_POWER,
    TARGET_RESISTANCE,
    TARGET_SPEED,
)
from ..errors import CharacteristicNotFound
from .machine_type import MachineType

_LOGGER = logging.getLogger(__name__)


class MovementDirection(IntEnum, boundary=STRICT):
    """
    Movement direction. Used by `CrossTrainer` machine only.

    Described in section **4.5.1.1 Flags Field**.
    """

    FORWARD = False
    """Move Forward"""
    BACKWARD = True
    """Move Backward"""


class MachineFeatures(IntFlag, boundary=STRICT):
    """
    Fitness Machine Features.

    Described in section `4.3.1.1: Fitness Machine Features Field`.
    """

    AVERAGE_SPEED = auto()
    """Average Speed"""
    CADENCE = auto()
    """Cadence"""
    DISTANCE = auto()
    """Total Distance"""
    INCLINATION = auto()
    """Inclination"""
    ELEVATION_GAIN = auto()
    """Elevation Gain"""
    PACE = auto()
    """Pace"""
    STEP_COUNT = auto()
    """Step Count"""
    RESISTANCE = auto()
    """Resistance Level"""
    STRIDE_COUNT = auto()
    """Stride Count"""
    EXPENDED_ENERGY = auto()
    """Expended Energy"""
    HEART_RATE = auto()
    """Heart Rate Measurement"""
    METABOLIC_EQUIVALENT = auto()
    """Metabolic Equivalent"""
    ELAPSED_TIME = auto()
    """Elapsed Time"""
    REMAINING_TIME = auto()
    """Remaining Time"""
    POWER_MEASUREMENT = auto()
    """Power Measurement"""
    FORCE_ON_BELT_AND_POWER_OUTPUT = auto()
    """Force on Belt and Power Output"""
    USER_DATA_RETENTION = auto()
    """User Data Retention"""


class MachineSettings(IntFlag, boundary=STRICT):
    """
    Target Setting Features.

    Described in section `4.3.1.2: Target Setting Features Field`.
    """

    SPEED = auto()
    """Speed Target"""
    INCLINE = auto()
    """Inclination Target"""
    RESISTANCE = auto()
    """Resistance Target"""
    POWER = auto()
    """Power Target"""
    HEART_RATE = auto()
    """Heart Rate Target"""
    ENERGY = auto()
    """Targeted Expended Energy"""
    STEPS = auto()
    """Targeted Step Number"""
    STRIDES = auto()
    """Targeted Stride Number"""
    DISTANCE = auto()
    """Targeted Distance"""
    TIME = auto()
    """Targeted Training Time"""
    TIME_TWO_ZONES = auto()
    """Targeted Time in Two Heart Rate Zones"""
    TIME_THREE_ZONES = auto()
    """Targeted Time in Three Heart Rate Zones"""
    TIME_FIVE_ZONES = auto()
    """Targeted Time in Five Heart Rate Zones"""
    BIKE_SIMULATION = auto()
    """Indoor Bike Simulation Parameters"""
    CIRCUMFERENCE = auto()
    """Wheel Circumference"""
    SPIN_DOWN = auto()
    """Spin Down Control"""
    CADENCE = auto()
    """Targeted Cadence"""


class SettingRange(NamedTuple):
    """Value range of settings parameter."""

    min_value: float
    """Minimum value. Included in the range."""
    max_value: float
    """Maximum value. Included in the range."""
    step: float
    """Step value."""


async def _read_range(
    cli: BleakClient, c: BleakGATTCharacteristic, format: str
) -> SettingRange:
    data = await cli.read_gatt_char(c)

    bio, serializer = io.BytesIO(data), NumSerializer(format)
    result = SettingRange(*(serializer.deserialize(bio) or 0 for _ in range(3)))

    assert not bio.read(1)
    return result


async def read_features(
    cli: BleakClient,
    mt: MachineType,
) -> tuple[
    MachineFeatures, MachineSettings, MappingProxyType[str, SettingRange]
]:
    _LOGGER.debug("Reading features and settings...")

    if (c := cli.services.get_characteristic(FEATURE_UUID)) is None:
        raise CharacteristicNotFound("Machine Feature")

    assert len(data := await cli.read_gatt_char(c)) == 8

    bio, u4 = io.BytesIO(data), NumSerializer("u4")

    features = MachineFeatures(u4.deserialize(bio))
    settings = MachineSettings(u4.deserialize(bio))

    # Remove untypical settings

    if MachineType.TREADMILL in mt:
        settings &= ~(MachineSettings.RESISTANCE | MachineSettings.POWER)

    elif MachineType.CROSS_TRAINER in mt:
        settings &= ~(MachineSettings.SPEED | MachineSettings.INCLINE)

    elif MachineType.INDOOR_BIKE in mt:
        settings &= ~(MachineSettings.SPEED | MachineSettings.INCLINE)

    elif MachineType.ROWER in mt:
        settings &= ~(MachineSettings.SPEED | MachineSettings.INCLINE)

    # Remove settings without ranges UUIDs

    ranges: dict[str, SettingRange] = {}

    if MachineSettings.SPEED in settings:
        if c := cli.services.get_characteristic(SPEED_RANGE_UUID):
            ranges[TARGET_SPEED] = await _read_range(cli, c, "u2.01")
        else:
            settings &= ~MachineSettings.SPEED
            _LOGGER.debug(
                "Speed setting has been removed. "
                "Characteristic with a range of acceptable values not found."
            )

    if MachineSettings.INCLINE in settings:
        if c := cli.services.get_characteristic(INCLINATION_RANGE_UUID):
            ranges[TARGET_INCLINATION] = await _read_range(cli, c, "s2.1")
        else:
            settings &= ~MachineSettings.INCLINE
            _LOGGER.debug(
                "Inclination setting has been removed. "
                "Characteristic with a range of acceptable values not found."
            )

    if MachineSettings.RESISTANCE in settings:
        if c := cli.services.get_characteristic(RESISTANCE_LEVEL_RANGE_UUID):
            ranges[TARGET_RESISTANCE] = await _read_range(cli, c, "s2.1")
        else:
            settings &= ~MachineSettings.RESISTANCE
            _LOGGER.debug(
                "Resistance setting has been removed. "
                "Characteristic with a range of acceptable values not found."
            )

    if MachineSettings.POWER in settings:
        if c := cli.services.get_characteristic(POWER_RANGE_UUID):
            ranges[TARGET_POWER] = await _read_range(cli, c, "s2")
        else:
            settings &= ~MachineSettings.POWER
            _LOGGER.debug(
                "Power setting has been removed. "
                "Characteristic with a range of acceptable values not found."
            )

    if MachineSettings.HEART_RATE in settings:
        if c := cli.services.get_characteristic(HEART_RATE_RANGE_UUID):
            ranges[TARGET_HEART_RATE] = await _read_range(cli, c, "u1")
        else:
            settings &= ~MachineSettings.HEART_RATE
            _LOGGER.debug(
                "Heart Rate setting has been removed. "
                "Characteristic with a range of acceptable values not found."
            )

    _LOGGER.debug("Features: %s", features)
    _LOGGER.debug("Settings: %s", settings)
    _LOGGER.debug("Settings ranges: %s", ranges)

    return features, settings, MappingProxyType(ranges)
