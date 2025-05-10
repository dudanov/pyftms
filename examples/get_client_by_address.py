# Based on https://github.com/hbldh/bleak/blob/develop/examples/service_explorer.py

import argparse
import asyncio

from bleak import BleakClient, BleakScanner
from bleak.uuids import normalize_uuid_str

from pyftms import get_client, FtmsEvents, MachineType
from pyftms.client import const

def on_event(event: FtmsEvents):
    print(f"event received: {event}")


def on_disconnect():
    print("machine disconnected")


async def run(args: argparse.Namespace):
    """Finds an FTMS device by address and sets up a client without advertisement data."""
    device = await BleakScanner.find_device_by_address(args.address)
    if device is None:
        print(f"could not find device with address {args.address}")
        return

    machine_type = None

    async with BleakClient(
        device,
        services=[normalize_uuid_str(const.FTMS_UUID)],
    ) as client:
        for service in client.services:
            for char in service.characteristics:
                if char.uuid == normalize_uuid_str(const.TREADMILL_DATA_UUID):
                    machine_type = MachineType.TREADMILL
                elif char.uuid == normalize_uuid_str(const.CROSS_TRAINER_DATA_UUID):
                    machine_type = MachineType.CROSS_TRAINER
                elif char.uuid == normalize_uuid_str(const.ROWER_DATA_UUID):
                    machine_type = MachineType.ROWER
                elif char.uuid == normalize_uuid_str(const.INDOOR_BIKE_DATA_UUID):
                    machine_type = MachineType.INDOOR_BIKE

    if machine_type is None:
        print("could not determine machine type")
        return

    async with get_client(
        ble_device=device,
        adv_or_type=machine_type,
        on_ftms_event=on_event,
        on_disconnect=on_disconnect,
    ) as c:
        print(f"machine name is {c.name}")
        print(f"machine type is {c.machine_type.name}")
        print(f"machine supported properties are {c.supported_properties}")
        print(f"machine supported settings are {c.supported_settings}")

        # Interact with the client here


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--address",
        metavar="<address>",
        help="the address of the bluetooth device to connect to",
        required=True,
    )

    asyncio.run(run(parser.parse_args()))
