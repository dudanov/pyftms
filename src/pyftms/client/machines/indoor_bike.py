# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

from typing import ClassVar

from ...models import IndoorBikeData, RealtimeData
from ..client import FitnessMachine
from ..const import INDOOR_BIKE_DATA_UUID
from ..properties import MachineType


class IndoorBike(FitnessMachine):
    """
    Indoor Bike (Spin Bike).

    Specific class of `FitnessMachine`.
    """

    _machine_type: ClassVar[MachineType] = MachineType.INDOOR_BIKE

    _data_model: ClassVar[type[RealtimeData]] = IndoorBikeData

    _data_uuid: ClassVar[str] = INDOOR_BIKE_DATA_UUID
