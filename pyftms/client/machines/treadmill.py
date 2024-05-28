# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

from typing import ClassVar

from ...models import RealtimeData, TreadmillData
from ..client import FitnessMachine
from ..const import TREADMILL_DATA_UUID
from ..properties import MachineType


class Treadmill(FitnessMachine):
    """
    Treadmill.

    Specific class of `FitnessMachine`.
    """

    _machine_type: ClassVar[MachineType] = MachineType.TREADMILL

    _data_model: ClassVar[type[RealtimeData]] = TreadmillData

    _data_uuid: ClassVar[str] = TREADMILL_DATA_UUID
