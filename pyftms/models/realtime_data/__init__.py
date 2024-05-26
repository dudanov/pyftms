# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import typing

from .common import RealtimeData
from .cross_trainer import CrossTrainerData
from .indoor_bike import IndoorBikeData
from .rower import RowerData
from .treadmill import TreadmillData

RealtimeDataT = typing.TypeVar("RealtimeDataT", bound=RealtimeData)


__all__ = [
    "CrossTrainerData",
    "IndoorBikeData",
    "RowerData",
    "TreadmillData",
    "RealtimeData",
    "RealtimeDataT",
]
