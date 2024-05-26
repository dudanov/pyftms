# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import logging
from enum import Flag, auto

from bleak.backends.scanner import AdvertisementData

from ..const import FITNESS_MACHINE_SERVICE_UUID

_LOGGER = logging.getLogger(__name__)


class MachineFlags(Flag):
    """
    Fitness Machine Flags.

    Included in the `Service Data AD Type`.

    Described in section `3.1.1: Flags Field`.
    """

    FITNESS_MACHINE = auto()
    """Fitness Machine Available"""


class MachineType(Flag):
    """
    Fitness Machine Type.

    Included in the `Service Data AD Type`.

    Described in section `3.1.2: Fitness Machine Type Field`.
    """

    TREADMILL = auto()
    """Treadmill Supported"""
    CROSS_TRAINER = auto()
    """Cross Trainer Supported"""
    STEP_CLIMBER = auto()
    """Step Climber Supported"""
    STAIR_CLIMBER = auto()
    """Stair Climber Supported"""
    ROWER = auto()
    """Rower Supported"""
    INDOOR_BIKE = auto()
    """Indoor Bike Supported"""


class NotFitnessMachineError(Exception):
    def __init__(self, adv_data: bytes | None) -> None:
        msg = "No service data"

        if adv_data is not None:
            msg = f"AD service data: '{adv_data.hex(" ")}'"

        super().__init__(f"Device is not Fitness Machine. {msg}.")


def get_machine_type_from_service_data(adv: AdvertisementData) -> MachineType:
    """Returns Fitness Machine Type from service AD data."""
    data = adv.service_data.get(FITNESS_MACHINE_SERVICE_UUID)

    if data is None or len(data) != 3:
        raise NotFitnessMachineError(data)

    # Reading mandatory `Flags` and `Machine Type`.
    # Machine Type bytes may be reversed on some
    # machines (it's bug), so I logically ORed them.
    try:
        mf, mt = MachineFlags(data[0]), MachineType(data[1] | data[2])

    except ValueError:
        raise NotFitnessMachineError(data)

    if mf and mt:
        return mt

    raise NotFitnessMachineError(data)
