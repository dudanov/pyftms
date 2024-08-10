# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import asyncio

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from bleak.exc import BleakDeviceNotFoundError

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
from .client import DisconnectCallback, FitnessMachine
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
    on_disconnect: DisconnectCallback | None = None,
) -> FitnessMachine:
    """
    Creates an `FitnessMachine` instance from [Bleak](https://bleak.readthedocs.io/) discovered
    information: device and advertisement data. Instead of advertisement data, the `MachineType` can be used.

    Parameters:
    - `ble_device` - [BLE device](https://bleak.readthedocs.io/en/latest/api/index.html#bleak.backends.device.BLEDevice).
    - `adv_or_type` - Service [advertisement data](https://bleak.readthedocs.io/en/latest/backends/index.html#bleak.backends.scanner.AdvertisementData) or `MachineType`.
    - `timeout` - Control operation timeout. Defaults to 2.0s.
    - `on_ftms_event` - Callback for receiving fitness machine events.
    - `on_disconnect` - Disconnection callback.

    Return:
    - `FitnessMachine` instance.
    """

    adv_data = None

    if isinstance(adv_or_type, AdvertisementData):
        adv_data = adv_or_type
        adv_or_type = get_machine_type_from_service_data(adv_or_type)

    cls = get_machine(adv_or_type)

    return cls(
        ble_device,
        adv_data,
        timeout=timeout,
        on_ftms_event=on_ftms_event,
        on_disconnect=on_disconnect,
    )


async def get_client_from_address(
    address: str,
    *,
    scan_timeout: float = 10.0,
    timeout: float = 2.0,
    on_ftms_event: FtmsCallback | None = None,
    on_disconnect: DisconnectCallback | None = None,
) -> FitnessMachine:
    """
    Scans for fitness machine with specified BLE address. On success creates and return an `FitnessMachine` instance.

    Parameters:
    - `address` - The Bluetooth address of the device on this machine (UUID on macOS).
    - `scan_timeout` - Scanning timeout. Defaults to 10.0s.
    - `timeout` - Control operation timeout. Defaults to 2.0s.
    - `on_ftms_event` - Callback for receiving fitness machine events.
    - `on_disconnect` - Disconnection callback.

    Return:
    - `FitnessMachine` instance if device found successfully.
    """

    async with BleakScanner() as scanner:
        try:
            async with asyncio.timeout(scan_timeout):
                async for dev, adv in scanner.advertisement_data():
                    if dev.address.lower() != address.lower():
                        continue

                    try:
                        return get_client(
                            dev,
                            adv,
                            timeout=timeout,
                            on_ftms_event=on_ftms_event,
                            on_disconnect=on_disconnect,
                        )

                    except NotFitnessMachineError:
                        pass

        except asyncio.TimeoutError:
            pass

    raise BleakDeviceNotFoundError(address)


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
    "DisconnectCallback",
]
