# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

from .common import (
    CodeSwitchModel,
    IndoorBikeSimulationParameters,
    StopPauseCode,
)
from .control_point import (
    ControlCode,
    ControlIndicateModel,
    ControlModel,
    ResultCode,
)
from .machine_status import MachineStatusCode, MachineStatusModel
from .realtime_data import (
    CrossTrainerData,
    IndoorBikeData,
    RealtimeData,
    RowerData,
    TreadmillData,
)
from .spin_down import (
    SpinDownControlCode,
    SpinDownSpeedData,
    SpinDownStatusCode,
)
from .training_status import (
    TrainingStatusCode,
    TrainingStatusFlags,
    TrainingStatusModel,
)

__all__ = [
    "CodeSwitchModel",
    "CrossTrainerData",
    "IndoorBikeData",
    "RowerData",
    "TreadmillData",
    "ControlCode",
    "ControlModel",
    "ControlIndicateModel",
    "SpinDownSpeedData",
    "IndoorBikeSimulationParameters",
    "MachineStatusCode",
    "MachineStatusModel",
    "ResultCode",
    "SpinDownControlCode",
    "SpinDownStatusCode",
    "StopPauseCode",
    "TrainingStatusCode",
    "TrainingStatusFlags",
    "TrainingStatusModel",
    "RealtimeData",
]
