# PyFTMS - Python Fitness Machine Service client library

**PyFTMS** is a Python client library for the **FTMS service**, which is a standard for fitness equipment with a Bluetooth interface. **Bleak** is used as the Bluetooth library. Currently four main types of fitness machines are supported:
 1. **Treadmill**
 2. **Cross Trainer** (Elliptical Trainer)
 3. **Rower** (Rowing Machine)
 4. **Indoor Bike** (Spin Bike)

**Step Climber** and **Stair Climber** machines are **not supported** due to incomplete protocol information and low popularity.

!!! **API** !!! not stable and may be unsignifically changed.

## Requirments

1. Python >= 3.11;
2. Bleak >= 0.22.

## Install it from PyPI

```bash
pip install pyftms
```

## Usage

With context manager:

```py
import asyncio
import logging

from ftms import get_client_from_address
from ftms.client.backends import FtmsEvents

ADDRESS = "BA:BA:DE:DA:CA:FE"

def on_event(event: FtmsEvents):
	print(f"New event: {event}")

async def run():
	async with await get_client_from_address(ADDRESS, on_event_callback=on_event) as c:
		properties = c.properties
		settings = c.settings
		print(f"Device Info: {c.device_info}")
		print(f"Supported: {c.supported_settings}")
		print(f"Supported: {c.supported_properties}")
		print(f"Available: {c.available_properties}")

		for  _  in  range(50):
			print(f"Properties: {properties}")
			print(f"Settings: {settings}")
			
			await  asyncio.sleep(10)

asyncio.run(run())
```
