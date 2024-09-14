# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import asyncio

from .client import discover_ftms_devices, get_client


async def run():
    print("Scanning for available FTMS devices...")

    lst = []

    async for dev, machine_type in discover_ftms_devices(discover_time=5):
        lst.append((dev, machine_type))

        print(
            f"{len(lst)}. {machine_type.name}: name: {dev.name}, address: {dev.address}"
        )

    for dev, machine_type in lst:
        print(
            f"\nConnection to {machine_type.name}: name: {dev.name}, address: {dev.address}"
        )

        async with get_client(dev, machine_type) as c:
            print(f" 1. Device Info: {c.device_info}")
            print(f" 2. Supported settings: {c.supported_settings}")
            print(f" 3. Supported properties: {c.supported_properties}")
            print(f" 4. Available properties: {c.available_properties}")

    print("\nDone.")


asyncio.run(run())
