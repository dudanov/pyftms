# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

from typing import ClassVar

from ...models import CrossTrainerData, RealtimeData
from ..client import FitnessMachine
from ..const import CROSS_TRAINER_DATA_UUID
from ..properties import MachineType


class CrossTrainer(FitnessMachine):
    """
    Cross Trainer (Elliptical Trainer).

    Specific class of `FitnessMachine`.
    """

    _machine_type: ClassVar[MachineType] = MachineType.CROSS_TRAINER

    _data_model: ClassVar[type[RealtimeData]] = CrossTrainerData

    _data_uuid: ClassVar[str] = CROSS_TRAINER_DATA_UUID
