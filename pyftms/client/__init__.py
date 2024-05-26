# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import asyncio

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from .backends import FtmsCallback
from .client import FitnessMachine
from .const import FITNESS_MACHINE_SERVICE_UUID
from .machines import get_machine
from .properties import (
    MachineType,
    NotFitnessMachineError,
    get_machine_type_from_service_data,
)


def get_client(
    ble_device: BLEDevice,
    adv_or_type: AdvertisementData | MachineType,
    *,
    timeout: float = 2.0,
    on_event_callback: FtmsCallback | None = None,
) -> FitnessMachine:
    if isinstance(adv_or_type, AdvertisementData):
        adv_or_type = get_machine_type_from_service_data(adv_or_type)
    cls = get_machine(adv_or_type)
    return cls(ble_device, on_event_callback=on_event_callback, timeout=timeout)


async def get_client_from_address(
    address: str,
    *,
    scan_timeout: float | None = None,
    timeout: float = 2.0,
    on_event_callback: FtmsCallback | None = None,
) -> FitnessMachine:
    future: asyncio.Future[tuple[BLEDevice, AdvertisementData]] = asyncio.Future()

    def _on_device(dev: BLEDevice, adv: AdvertisementData) -> None:
        if not future.done() and dev.address.lower() == address.lower():
            future.set_result((dev, adv))

    scanner = BleakScanner(_on_device, [FITNESS_MACHINE_SERVICE_UUID])

    await scanner.start()

    try:
        dev, adv = await asyncio.wait_for(future, scan_timeout)
        return get_client(
            dev, adv, on_event_callback=on_event_callback, timeout=timeout
        )
    finally:
        await scanner.stop()


__all__ = [
    "get_client",
    "get_client_from_address",
    "MachineType",
    "NotFitnessMachineError",
]
