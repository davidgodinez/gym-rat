import asyncio
import aiohttp
from flask import Flask, jsonify

app = Flask(__name__)

data = {}


async def get_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://example.com/data') as response:
            data = await response.json()
    return data


async def update_data():
    while True:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://example.com/data') as response:
                data = await response.json()
        await asyncio.sleep(60)


@app.route('/')
async def index():
    return jsonify(data)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(update_data())
    app.run()
