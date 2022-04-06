# Testing python client

# Install
# pip install "python-socketio[asyncio_client]"

import asyncio
import socketio

async def run():

    sio = socketio.AsyncClient()

    @sio.event
    def connect():
        print('connection established')

    @sio.on('message')
    def on_message(data):
        print('chat message:', data)

    async def send_message(data):
        await sio.emit('message', data)

    await sio.connect('http://michael.zt:3000')
    await send_message("Hello, I came from Python!")
    await sio.wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())