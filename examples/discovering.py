# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import asyncio

from pyftms import discover_ftms_devices


async def run():
    async for dev, machine_type in discover_ftms_devices():
        print(
            f"Found {machine_type.name}: name: {dev.name}, address: {dev.address}"
        )


asyncio.run(run())
