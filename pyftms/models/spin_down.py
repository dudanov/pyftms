# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import dataclasses as dc
from enum import STRICT, IntEnum, auto

from .common import BaseModel, model_meta


class SpinDownStatusCode(IntEnum, boundary=STRICT):
    """
    Spin Down Status.

    Described in section `4.17 Fitness Machine Status. Table 4.27`.
    """

    REQUESTED = auto()
    """Spin Down Requested"""

    SUCCESS = auto()
    """Success"""

    ERROR = auto()
    """Error"""

    STOP_PEDALING = auto()
    """Stop Pedaling"""


class SpinDownControlCode(IntEnum, boundary=STRICT):
    """
    Spin Down Status.

    Described in section `4.17 Fitness Machine Status. Table 4.27`.
    """

    START = auto()
    """Spin Down Requested"""

    IGNORE = auto()
    """Success"""


@dc.dataclass(frozen=True)
class SpinDownSpeedData(BaseModel):
    """
    Response Parameter when the Spin Down Procedure succeeds.

    Described in section `4.16.2.20 Spin Down Control Procedure`.
    """

    low: float = dc.field(
        metadata=model_meta(
            format="u2.01",
        )
    )
    """Target Speed Low | km/h"""

    high: float = dc.field(
        metadata=model_meta(
            format="u2.01",
        )
    )
    """Target Speed High | km/h"""
