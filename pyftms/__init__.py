# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

from typing import TypeVar

from .client import (
    FitnessMachine,
    FtmsCallback,
    get_client,
    get_client_from_address,
    get_machine,
    get_machine_type_from_service_data,
)
from .client.machines import CrossTrainer, IndoorBike, Rower, Treadmill
from .client.backends import FtmsEvents

FitnessMachineT = TypeVar("FitnessMachineT", bound=FitnessMachine)


__all__ = [
    "get_client",
    "get_client_from_address",
    "get_machine",
    "get_machine_type_from_service_data",
    "FtmsCallback",
    "IndoorBike",
    "Treadmill",
    "Rower",
    "CrossTrainer",
    "FitnessMachine",
    "FitnessMachineT",
    "FtmsEvents",
]
