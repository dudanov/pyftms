# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import logging
from abc import ABC
from types import MappingProxyType
from typing import ClassVar, Generic, TypeVar

from bleak import BleakClient
from bleak.backends.device import BLEDevice
from bleak_retry_connector import (
    BleakClientWithServiceCache,
    close_stale_connections,
    establish_connection,
)

from ..models import (
    ControlCode,
    ControlModel,
    IndoorBikeSimulationParameters,
    RealtimeData,
    ResultCode,
    SpinDownControlCode,
    StopPauseCode,
)
from .backends import DataUpdater, FtmsCallback, MachineController
from .manager import PropertiesManager
from .properties import (
    DeviceInfo,
    MachineFeatures,
    MachineSettings,
    MachineType,
    SettingRange,
    read_device_info,
    read_features,
    read_supported_ranges,
)

_LOGGER = logging.getLogger(__name__)

RealtimeDataT = TypeVar("RealtimeDataT", bound=RealtimeData)


class FitnessMachine(ABC, Generic[RealtimeDataT], PropertiesManager):
    _machine_type: ClassVar[MachineType]
    """Machine type."""

    _data_model: type[RealtimeDataT]
    """Model of real-time training data."""

    _data_uuid: ClassVar[str]
    """Notify UUID of real-time training data."""

    _cli: BleakClientWithServiceCache | None = None

    _data_updater: DataUpdater[RealtimeDataT]

    # Static device info

    _device: BLEDevice
    _device_info: DeviceInfo
    _m_features: MachineFeatures
    _m_settings: MachineSettings
    _settings_ranges: MappingProxyType[str, SettingRange]

    def __init__(
        self,
        ble_device: BLEDevice,
        *,
        timeout: float = 2.0,
        on_event_callback: FtmsCallback | None = None,
    ) -> None:
        super().__init__(on_event_callback)

        self._device = ble_device
        self._timeout = timeout

        # Updaters
        self._data_updater = DataUpdater(self._data_model, self._on_event)
        self._controller = MachineController(self._on_event)

    def _get_supported_properties(self, features: MachineFeatures) -> tuple[str, ...]:
        return self._data_model._get_features(features)

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()

    # BLE SPECIFIC PROPERTIES

    @property
    def address(self) -> str:
        return self._device.address

    @property
    def is_connected(self) -> bool:
        return self._cli is not None and self._cli.is_connected

    async def connect(self):
        await self._connect()

    async def disconnect(self) -> None:
        if self.is_connected:
            assert self._cli
            await self._disable_updates()
            await self._cli.disconnect()

    # COMMON BASE PROPERTIES

    @property
    def device_info(self) -> DeviceInfo:
        return self._device_info

    @property
    def machine_type(self) -> MachineType:
        return self._machine_type

    @property
    def machine_features(self) -> MachineFeatures:
        return self._m_features

    @property
    def supported_properties(self) -> tuple[str, ...]:
        """
        Properties that supported by this machine.
        Based on `Machine Features` report.

        May contain both meaningless properties and may not contain
        some properties that are supported by the machine.
        """
        return self._get_supported_properties(self._m_features)

    @property
    def available_properties(self) -> tuple[str, ...]:
        """All properties that MAY BE supported by this machine type."""
        return self._get_supported_properties(MachineFeatures(~0))

    @property
    def machine_settings(self) -> MachineSettings:
        return self._m_settings

    @property
    def supported_settings(self) -> tuple[str, ...]:
        return ControlModel._get_features(self._m_settings)

    @property
    def supported_ranges(self) -> MappingProxyType[str, SettingRange]:
        return self._settings_ranges

    async def _enable_updates(self) -> None:
        assert self._cli
        await self._controller.subscribe(self._cli)
        await self._data_updater.subscribe(self._cli, self._data_uuid)

    async def _disable_updates(self) -> None:
        assert self._cli
        await self._data_updater.unsubscribe(self._cli, self._data_uuid)
        await self._controller.unsubscribe(self._cli)

    async def _connect(self) -> None:
        """Initialize connection and read necessary data from device."""

        if self.is_connected:
            return

        _LOGGER.debug("Initialization. Trying to establish connection.")

        name = getattr(self._device, "name", "Generic FTMS")

        await close_stale_connections(self._device)

        self._cli = await establish_connection(
            BleakClientWithServiceCache,
            self._device,
            name,
            disconnected_callback=self._on_disconnect,
        )

        _LOGGER.debug("Connection success.")

        # Reading necessary static fitness machine information

        if not hasattr(self, "_device_info"):
            self._device_info = await read_device_info(self._cli)

        if not hasattr(self, "_features"):
            self._m_features, self._m_settings = await read_features(self._cli)

        if not hasattr(self, "_settings_ranges"):
            self._settings_ranges = await read_supported_ranges(
                self._cli, self._m_settings
            )

        await self._enable_updates()

    def _on_disconnect(self, cli: BleakClient) -> None:
        """BLE disconnect handler."""
        _LOGGER.debug("Client is disconnected. Reset updaters states.")
        self._cli = None
        self._data_updater.reset()
        self._controller.reset()

    # COMMANDS

    async def _write_command(self, code: ControlCode | None = None, *args, **kwargs):
        assert self._cli
        return await self._controller.write_command(
            self._cli, code, timeout=self._timeout, **kwargs
        )

    async def reset(self) -> ResultCode:
        return await self._write_command(ControlCode.RESET)

    async def start(self) -> ResultCode:
        return await self._write_command(ControlCode.START_RESUME)

    async def stop(self) -> ResultCode:
        return await self._write_command(stop_pause=StopPauseCode.STOP)

    async def pause(self) -> ResultCode:
        return await self._write_command(stop_pause=StopPauseCode.PAUSE)

    async def set_target_speed(self, value: float) -> ResultCode:
        return await self._write_command(target_speed=value)

    async def set_target_inclination(self, value: float) -> ResultCode:
        return await self._write_command(target_inclination=value)

    async def set_target_resistance(self, value: float) -> ResultCode:
        return await self._write_command(target_resistance=value)

    async def set_target_power(self, value: int) -> ResultCode:
        return await self._write_command(target_power=value)

    async def set_target_heart_rate(self, value: int) -> ResultCode:
        return await self._write_command(target_heart_rate=value)

    async def set_target_energy(self, value: int) -> ResultCode:
        return await self._write_command(target_energy=value)

    async def set_target_steps(self, value: int) -> ResultCode:
        return await self._write_command(target_steps=value)

    async def set_target_strides(self, value: int) -> ResultCode:
        return await self._write_command(target_strides=value)

    async def set_target_distance(self, value: int) -> ResultCode:
        return await self._write_command(target_distance=value)

    async def set_target_time(self, *value: int) -> ResultCode:
        return await self._write_command(code=None, target_time=value)

    async def set_bike_simulation_params(
        self, p: IndoorBikeSimulationParameters
    ) -> ResultCode:
        return await self._write_command(indoor_bike_simulation=p)

    async def set_wheel_circumference(self, value: float) -> ResultCode:
        return await self._write_command(wheel_circumference=value)

    async def spin_down_start(self) -> ResultCode:
        return await self._write_command(spin_down_control=SpinDownControlCode.START)

    async def spin_down_ignore(self) -> ResultCode:
        return await self._write_command(spin_down_control=SpinDownControlCode.IGNORE)

    async def set_target_cadence(self, value: float) -> ResultCode:
        return await self._write_command(target_cadence=value)
