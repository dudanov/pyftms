# Copyright 2024, Sergey Dudanov
# SPDX-License-Identifier: Apache-2.0

import asyncio
import logging

from .client import get_client_from_address
from .client.backends import FtmsEvents

ADDRESS = "FA:33:34:61:F4:68"

logging.basicConfig(level=logging.DEBUG)

_LOGGER = logging.getLogger(__name__)


def on_event(event: FtmsEvents):
    print(f"New event: {event}")


async def run():
    async with await get_client_from_address(ADDRESS, on_ftms_event=on_event) as c:
        properties = c.properties
        settings = c.settings

        print(f"Device Info: {c.device_info}")
        print(f"Supported: {c.supported_settings}")
        print(f"Supported: {c.supported_properties}")
        print(f"Available: {c.available_properties}")

        for _ in range(50):
            print()
            print(f"Properties: {properties}")
            print(f"Settings: {settings}")

            await asyncio.sleep(10)


asyncio.run(run())
