# Copyright 2024-2025, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import logging
from abc import ABC
from functools import cached_property
from types import MappingProxyType
from typing import Any, Callable, ClassVar

from bleak import BleakClient
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from bleak_retry_connector import close_stale_connections, establish_connection

from ..models import (
    ControlCode,
    ControlModel,
    IndoorBikeSimulationParameters,
    RealtimeData,
    ResultCode,
    SpinDownControlCode,
    StopPauseCode,
)
from . import const as c
from .backends import DataUpdater, FtmsCallback, MachineController, UpdateEvent
from .manager import PropertiesManager
from .properties import (
    DeviceInfo,
    MachineFeatures,
    MachineSettings,
    MachineType,
    SettingRange,
    read_device_info,
    read_features,
)
from .properties.device_info import DIS_UUID

_LOGGER = logging.getLogger(__name__)

type DisconnectCallback = Callable[[FitnessMachine], None]


class FitnessMachine(ABC, PropertiesManager):
    """
    Base FTMS client.

    Supports `async with ...` context manager.
    """

    _machine_type: ClassVar[MachineType]
    """Machine type."""

    _data_model: ClassVar[type[RealtimeData]]
    """Model of real-time training data."""

    _data_uuid: ClassVar[str]
    """Notify UUID of real-time training data."""

    _cli: BleakClient

    _updater: DataUpdater

    _device: BLEDevice
    _need_connect: bool

    # Static device info

    _device_info: DeviceInfo
    _m_features: MachineFeatures
    _m_settings: MachineSettings
    _settings_ranges: MappingProxyType[str, SettingRange]

    def __init__(
        self,
        ble_device: BLEDevice,
        adv_data: AdvertisementData | None = None,
        *,
        timeout: float = 2.0,
        on_ftms_event: FtmsCallback | None = None,
        on_disconnect: DisconnectCallback | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(on_ftms_event)

        self._need_connect = False
        self._timeout = timeout
        self._disconnect_cb = on_disconnect
        self._kwargs = kwargs

        self.set_ble_device_and_advertisement_data(ble_device, adv_data)

        # Updaters
        self._updater = DataUpdater(self._data_model, self._on_event)
        self._controller = MachineController(self._on_event)

    @classmethod
    def _get_supported_properties(
        cls, features: MachineFeatures = MachineFeatures(~0)
    ) -> list[str]:
        return cls._data_model._get_features(features)

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.disconnect()

    # BLE SPECIFIC PROPERTIES

    def set_ble_device_and_advertisement_data(
        self, ble_device: BLEDevice, adv_data: AdvertisementData | None
    ):
        self._device = ble_device

        if adv_data:
            self._properties["rssi"] = adv_data.rssi

            if self._cb:
                self._cb(UpdateEvent("update", {"rssi": adv_data.rssi}))

    @property
    def need_connect(self) -> bool:
        """Connection state latch. `True` if connection is needed."""
        return self._need_connect

    @need_connect.setter
    def need_connect(self, value: bool) -> None:
        """Connection state latch. `True` if connection is needed."""
        self._need_connect = value

    @property
    def rssi(self) -> int | None:
        """RSSI."""
        return self.get_property("rssi")

    @property
    def name(self) -> str:
        """Device name or BLE address"""

        return self._device.name or self._device.address

    def set_disconnect_callback(self, cb: DisconnectCallback):
        """Set disconnect callback."""
        self._disconnect_cb = cb

    async def connect(self) -> None:
        """
        Opens a connection to the device. Reads necessary static information:
        * Device Information (manufacturer, model, serial number, hardware and software versions);
        * Supported features;
        * Supported settings;
        * Ranges of parameters settings.
        """

        self._need_connect = True

        await self._connect()

    async def disconnect(self) -> None:
        """Disconnects from device."""

        self._need_connect = False

        if self.is_connected:
            await self._cli.disconnect()

    @property
    def address(self) -> str:
        """Bluetooth address."""

        return self._device.address

    @property
    def is_connected(self) -> bool:
        """Current connection status."""

        return hasattr(self, "_cli") and self._cli.is_connected

    # COMMON BASE PROPERTIES

    @property
    def device_info(self) -> DeviceInfo:
        """Device Information."""
        return self._device_info

    @property
    def machine_type(self) -> MachineType:
        """Machine type."""
        return self._machine_type

    @cached_property
    def supported_properties(self) -> tuple[str, ...]:
        """
        Properties that supported by this machine.
        Based on **Machine Features** report.

        *May contain both meaningless properties and may not contain
        some properties that are supported by the machine.*
        """
        x = self._get_supported_properties(self._m_features)
        if self.training_status is not None:
            x.append(c.TRAINING_STATUS)
        return tuple(x)

    @cached_property
    def available_properties(self) -> tuple[str, ...]:
        """All properties that *MAY BE* supported by this machine type."""
        x = self._get_supported_properties()
        x.append(c.TRAINING_STATUS)
        return tuple(x)

    @cached_property
    def supported_settings(self) -> tuple[str, ...]:
        """Supported settings."""
        return tuple(ControlModel._get_features(self._m_settings))

    @property
    def supported_ranges(self) -> MappingProxyType[str, SettingRange]:
        """Ranges of supported settings."""
        return self._settings_ranges

    def _on_disconnect(self, cli: BleakClient) -> None:
        _LOGGER.debug("Client disconnected. Reset updaters states.")

        del self._cli
        self._updater.reset()
        self._controller.reset()

        if self._disconnect_cb:
            self._disconnect_cb(self)

    async def _connect(self) -> None:
        if not self._need_connect or self.is_connected:
            return

        await close_stale_connections(self._device)

        _LOGGER.debug("Initialization. Trying to establish connection.")

        self._cli = await establish_connection(
            client_class=BleakClient,
            device=self._device,
            name=self.name,
            disconnected_callback=self._on_disconnect,
            # we needed only two services: `Fitness Machine Service` and `Device Information Service`
            services=[c.FTMS_UUID, DIS_UUID],
            kwargs=self._kwargs,
        )

        _LOGGER.debug("Connection success.")

        # Reading necessary static fitness machine information

        if not hasattr(self, "_device_info"):
            self._device_info = await read_device_info(self._cli)

        if not hasattr(self, "_features"):
            (
                self._m_features,
                self._m_settings,
                self._settings_ranges,
            ) = await read_features(self._cli, self._machine_type)

        await self._controller.subscribe(self._cli)
        await self._updater.subscribe(self._cli, self._data_uuid)

    # COMMANDS

    async def _write_command(self, code: ControlCode | None = None, *args, **kwargs):
        if self._need_connect:
            await self._connect()
            return await self._controller.write_command(
                self._cli, code, timeout=self._timeout, **kwargs
            )

        return ResultCode.FAILED

    async def reset(self) -> ResultCode:
        """Initiates the procedure to reset the controllable settings of a fitness machine."""
        return await self._write_command(ControlCode.RESET)

    async def start_resume(self) -> ResultCode:
        """Initiate the procedure to start or resume a training session."""
        return await self._write_command(ControlCode.START_RESUME)

    async def stop(self) -> ResultCode:
        """Initiate the procedure to stop a training session."""
        return await self._write_command(stop_pause=StopPauseCode.STOP)

    async def pause(self) -> ResultCode:
        """Initiate the procedure to pause a training session."""
        return await self._write_command(stop_pause=StopPauseCode.PAUSE)

    async def set_setting(self, setting_id: str, *args: Any) -> ResultCode:
        """
        Generic method of settings by ID.

        **Methods for setting specific parameters.**
        """

        if setting_id not in self.supported_settings:
            return ResultCode.NOT_SUPPORTED

        if not args:
            raise ValueError("No data to pass.")

        if len(args) == 1:
            args = args[0]

        return await self._write_command(code=None, **{setting_id: args})

    async def set_target_speed(self, value: float) -> ResultCode:
        """
        Sets target speed.

        Units: `km/h`.
        """
        return await self.set_setting(c.TARGET_SPEED, value)

    async def set_target_inclination(self, value: float) -> ResultCode:
        """
        Sets target inclination.

        Units: `%`.
        """
        return await self.set_setting(c.TARGET_INCLINATION, value)

    async def set_target_resistance(self, value: float) -> ResultCode:
        """
        Sets target resistance level.

        Units: `unitless`.
        """
        return await self.set_setting(c.TARGET_RESISTANCE, value)

    async def set_target_power(self, value: int) -> ResultCode:
        """
        Sets target power.

        Units: `Watt`.
        """
        return await self.set_setting(c.TARGET_POWER, value)

    async def set_target_heart_rate(self, value: int) -> ResultCode:
        """
        Sets target heart rate.

        Units: `bpm`.
        """
        return await self.set_setting(c.TARGET_HEART_RATE, value)

    async def set_target_energy(self, value: int) -> ResultCode:
        """
        Sets target expended energy.

        Units: `kcal`.
        """
        return await self.set_setting(c.TARGET_ENERGY, value)

    async def set_target_steps(self, value: int) -> ResultCode:
        """
        Sets targeted number of steps.

        Units: `step`.
        """
        return await self.set_setting(c.TARGET_STEPS, value)

    async def set_target_strides(self, value: int) -> ResultCode:
        """
        Sets targeted number of strides.

        Units: `stride`.
        """
        return await self.set_setting(c.TARGET_STRIDES, value)

    async def set_target_distance(self, value: int) -> ResultCode:
        """
        Sets targeted distance.

        Units: `m`.
        """
        return await self.set_setting(c.TARGET_DISTANCE, value)

    async def set_target_time(self, *value: int) -> ResultCode:
        """
        Set targeted training time.

        Units: `s`.
        """
        return await self.set_setting(c.TARGET_TIME, *value)

    async def set_indoor_bike_simulation(
        self,
        value: IndoorBikeSimulationParameters,
    ) -> ResultCode:
        """Set indoor bike simulation parameters."""
        return await self.set_setting(c.INDOOR_BIKE_SIMULATION, value)

    async def set_wheel_circumference(self, value: float) -> ResultCode:
        """
        Set wheel circumference.

        Units: `mm`.
        """
        return await self.set_setting(c.WHEEL_CIRCUMFERENCE, value)

    async def spin_down_start(self) -> ResultCode:
        """
        Start Spin-Down.

        It can be sent either in response to a request to start Spin-Down, or separately.
        """
        return await self.set_setting(c.SPIN_DOWN, SpinDownControlCode.START)

    async def spin_down_ignore(self) -> ResultCode:
        """
        Ignore Spin-Down.

        It can be sent in response to a request to start Spin-Down.
        """
        return await self.set_setting(c.SPIN_DOWN, SpinDownControlCode.IGNORE)

    async def set_target_cadence(self, value: float) -> ResultCode:
        """
        Set targeted cadence.

        Units: `rpm`.
        """
        return await self.set_setting(c.TARGET_CADENCE, value)
