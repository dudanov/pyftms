# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

from ..client import FitnessMachine
from ..properties import MachineType
from .cross_trainer import CrossTrainer
from .indoor_bike import IndoorBike
from .rower import Rower
from .treadmill import Treadmill


def get_machine(mt: MachineType) -> type[FitnessMachine]:
    """Returns Fitness Machine by type."""
    assert len(mt) == 1

    match mt:
        case MachineType.TREADMILL:
            return Treadmill

        case MachineType.CROSS_TRAINER:
            return CrossTrainer

        case MachineType.ROWER:
            return Rower

        case MachineType.INDOOR_BIKE:
            return IndoorBike

    raise NotImplementedError("This Fitness Machine type is not supported.")


__all__ = [
    "CrossTrainer",
    "IndoorBike",
    "Rower",
    "Treadmill",
    "get_machine",
]
