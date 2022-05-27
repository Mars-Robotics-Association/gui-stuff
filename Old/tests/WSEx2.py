import threading
import asyncio
import websockets
import logging
import json
import signal
import dearpygui.dearpygui as dpg
series_id = dpg.generate_uuid()

class RobotPosition:
    def __init__(self):
        self.xx = 0
        self.yy = 0
        self._lock = threading.Lock()

    def update(self, newx, newy):
        with self._lock:
            self.xx = newx
            self.yy = newy
            dpg.set_value(series_id, newy)



rp = RobotPosition()
loop = asyncio.new_event_loop()



async def consumer_handler(websocket) -> None:
    async for message in websocket:
        data = json.loads(message)
        rp.update(data['xx'], data['yy'])


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
    loop.run_until_complete(consume(hostname="192.168.43.1", port=8000))
    loop.close()


x = threading.Thread(target=tfunc)
x.daemon = True
x.start()

with dpg.window(label="Test", height=500, width=500):
    dpg.add_text("No Requests Yet", id=series_id)

dpg.setup_viewport()
dpg.start_dearpygui()

print("EXITED DEAR PY GUI")

try:
    for task in asyncio.all_tasks(loop):
        task.cancel()
except asyncio.CancelledError:
    pass

