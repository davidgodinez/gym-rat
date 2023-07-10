import asyncio
from bleak import BleakClient

device_address = "ED:5E:20:E7:2B:A1"  # Replace with your device's address
REPCOUNT_UUID = "17c73c1a-4bc7-11ed-bdc3-0242ac120002"  # Replace with your characteristic UUID

async def run():
    async with BleakClient(device_address) as client:
        print(f"Connected: {client.is_connected}")

        # Read the repCountCharacteristic
        repCount = await client.read_gatt_char(REPCOUNT_UUID)
        print(f"Rep count: {int.from_bytes(repCount, byteorder='little')}")

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

if __name__ == "__main__":
    main()
