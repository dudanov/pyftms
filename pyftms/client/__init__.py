# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import asyncio

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from .backends import (
    ControlEvent,
    FtmsCallback,
    SetupEvent,
    SetupEventData,
    SpinDownEvent,
    SpinDownEventData,
    TrainingStatusEvent,
    TrainingStatusEventData,
    UpdateEvent,
    UpdateEventData,
)
from .client import FitnessMachine
from .const import FITNESS_MACHINE_SERVICE_UUID
from .machines import get_machine
from .manager import PropertiesManager
from .properties import (
    DeviceInfo,
    MachineType,
    MovementDirection,
    NotFitnessMachineError,
    SettingRange,
    get_machine_type_from_service_data,
)


def get_client(
    ble_device: BLEDevice,
    adv_or_type: AdvertisementData | MachineType,
    *,
    timeout: float = 2.0,
    on_ftms_event: FtmsCallback | None = None,
) -> FitnessMachine:
    """
    Creates an `FitnessMachine` instance from [Bleak](https://bleak.readthedocs.io/) discovered
    information: device and advertisement data. Instead of advertisement data, the `MachineType` can be used.

    Parameters:
    - `ble_device` - [BLE device](https://bleak.readthedocs.io/en/latest/api/index.html#bleak.backends.device.BLEDevice).
    - `adv_or_type` - Service [advertisement data](https://bleak.readthedocs.io/en/latest/backends/index.html#bleak.backends.scanner.AdvertisementData) or `MachineType`.
    - `timeout` - Control operation timeout. Defaults to 2.0s.
    - `on_ftms_event` - Callback for receiving fitness machine events.

    Return:
    - `FitnessMachine` instance.
    """

    if isinstance(adv_or_type, AdvertisementData):
        adv_or_type = get_machine_type_from_service_data(adv_or_type)

    cls = get_machine(adv_or_type)

    return cls(ble_device, on_ftms_event=on_ftms_event, timeout=timeout)


async def get_client_from_address(
    address: str,
    *,
    scan_timeout: float = 10.0,
    timeout: float = 2.0,
    on_ftms_event: FtmsCallback | None = None,
) -> FitnessMachine:
    """
    Scans for fitness machine with specified BLE address. On success creates and return an `FitnessMachine` instance.

    Parameters:
    - `address` - The Bluetooth address of the device on this machine (UUID on macOS).
    - `scan_timeout` - Scanning timeout. Defaults to 10.0s.
    - `timeout` - Control operation timeout. Defaults to 2.0s.
    - `on_ftms_event` - Callback for receiving fitness machine events.

    Return:
    - `FitnessMachine` instance.
    """

    future: asyncio.Future[tuple[BLEDevice, AdvertisementData]] = asyncio.Future()

    def _on_device(dev: BLEDevice, adv: AdvertisementData) -> None:
        if not future.done() and dev.address.lower() == address.lower():
            future.set_result((dev, adv))

    scanner = BleakScanner(_on_device, [FITNESS_MACHINE_SERVICE_UUID])

    await scanner.start()

    try:
        dev, adv = await asyncio.wait_for(future, scan_timeout)
        return get_client(dev, adv, on_ftms_event=on_ftms_event, timeout=timeout)
    finally:
        await scanner.stop()


__all__ = [
    "get_client",
    "get_client_from_address",
    "MachineType",
    "NotFitnessMachineError",
    "UpdateEvent",
    "SetupEvent",
    "ControlEvent",
    "TrainingStatusEvent",
    "SpinDownEvent",
    "FtmsCallback",
    "SetupEventData",
    "UpdateEventData",
    "SpinDownEventData",
    "TrainingStatusEventData",
    "MovementDirection",
    "DeviceInfo",
    "SettingRange",
    "PropertiesManager",
]
