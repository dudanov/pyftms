# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

from typing import ClassVar

from ...models import RealtimeData, RowerData
from ..client import FitnessMachine
from ..const import ROWER_DATA_UUID
from ..properties import MachineType


class Rower(FitnessMachine):
    """
    Rower (Rowing Machine).

    Specific class of `FitnessMachine`.
    """

    _machine_type: ClassVar[MachineType] = MachineType.ROWER

    _data_model: ClassVar[type[RealtimeData]] = RowerData

    _data_uuid: ClassVar[str] = ROWER_DATA_UUID
