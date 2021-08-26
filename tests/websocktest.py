import time

from dearpygui import *
from dearpygui import *
import threading
import asyncio
import websockets
import logging
import json
import signal


class RobotPosition:
    def __init__(self):
        self.xx = 0
        self.yy = 0
        self._lock = threading.Lock()

    def update(self, newx, newy):
        with self._lock:
            self.xx = newx
            self.yy = newy


rp = RobotPosition()
loop = asyncio.new_event_loop()



async def consumer_handler(websocket) -> None:
    async for message in websocket:
        data = json.loads(message)
        #rp.update(data['xx'], data['yy'])
        print(data['xx'])


async def consume(hostname: str, port: int) -> None:
    websocket_resource_url = f"ws://{hostname}:{port}"
    async with websockets.connect(websocket_resource_url, ping_interval=5) as websocket:
        try:
            await consumer_handler(websocket)
        except asyncio.CancelledError:
            pass


def tfunc():
    # logger = logging.getLogger('websockets')
    # logger.setLevel(logging.DEBUG)
    # logger.addHandler(logging.StreamHandler())
    asyncio.set_event_loop(loop)
    loop.run_until_complete(consume(hostname="192.168.43.1", port=8001))
    loop.close()


x = threading.Thread(target=tfunc)
x.daemon = True
x.start()

print("EXITED DEAR PY GUI")
try:
    for task in asyncio.all_tasks(loop):
        task.cancel()
except asyncio.CancelledError:
    pass

