import asyncio
from bleak import BleakClient

async def run(address):
    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")

        services = await client.get_services()
        print("Services:")
        for service in services:
            print(service)

        characteristic = "fff1"
        value = await client.read_gatt_char(characteristic)
        print(f"Characteristic value: {value}")

loop = asyncio.get_event_loop()
# Replace with the address of your Arduino
loop.run_until_complete(run("ED:5E:20:E7:2B:A1"))
