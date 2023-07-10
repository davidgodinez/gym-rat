import asyncio
from bleak import BleakClient

async def connect(address):
    client = BleakClient(address)
    try:
        await asyncio.wait_for(client.connect(), timeout=10.0)
        print(f"Connected: {client.is_connected}")
    except asyncio.TimeoutError:
        print("Connection attempt timed out")
    finally:
        if client.is_connected:
            await client.disconnect()

address = "ED:5E:20:E7:2B:A1"
asyncio.run(connect(address))
