# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import logging
from typing import TypedDict

from bleak import BleakClient
from bleak.uuids import normalize_uuid_16

_DIS_UUID = 0x180A

_UUID_MAP: dict[str, int] = {
    "manufacturer": 0x2A29,
    "model": 0x2A24,
    "serial_number": 0x2A25,
    "sw_version": 0x2A28,
    "hw_version": 0x2A27,
}

_LOGGER = logging.getLogger(__name__)


class DeviceInfo(TypedDict, total=False):
    manufacturer: str
    model: str
    serial_number: str
    sw_version: str
    hw_version: str


async def read_device_info(cli: BleakClient) -> DeviceInfo:
    """Read Device Information."""

    _LOGGER.debug("Reading Device Information.")

    result = DeviceInfo()

    if srv := cli.services.get_service(normalize_uuid_16(_DIS_UUID)):
        for k, v in _UUID_MAP.items():
            if c := srv.get_characteristic(normalize_uuid_16(v)):
                data = await cli.read_gatt_char(c)
                result[k] = data.decode()

    _LOGGER.debug(f"Device Info: {result}.")

    return result
