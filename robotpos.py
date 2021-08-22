import dearpygui.dearpygui as dpg
import threading
import asyncio
import websockets
import logging
import json
import signal
myCircle = dpg.generate_uuid()
me = dpg.generate_uuid()

class RobotPosition:
    def __init__(self):
        self.xx = 0
        self.yy = 0
        self._lock = threading.Lock()

    def update(self, newx, newy):
        with self._lock:
            self.xx = newx
            self.yy = newy
            dpg.delete_item(me, children_only=True)
            dpg.draw_circle([150, 150], 50, thickness=10, color=(255, 0, 255), parent=me, id=myCircle)



rp = RobotPosition()
loop = asyncio.new_event_loop()

def testFunction():
    print('hey!')

with dpg.window(label="Window", height=750, width=850):
    with dpg.drawlist(width=800, height=500,id=me, callback=testFunction):
        newCircle = dpg.draw_circle([150, 150], 50, thickness=10, color=(255,0,255), id=myCircle,label="myCircle")
        dpg.configure_item(newCircle, center=[150,450])


async def consumer_handler(websocket) -> None:
    async for message in websocket:
        data = json.loads(message)
        print(data)
        #rp.update(data['xx'], data['yy'])


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
    loop.run_until_complete(consume(hostname="192.168.43.154", port=8000))
    loop.close()


x = threading.Thread(target=tfunc)
x.daemon = True
x.start()

#dpg.start_dearpygui()

print("EXITED DEAR PY GUI")
try:
    for task in asyncio.all_tasks(loop):
        task.cancel()
except asyncio.CancelledError:
    pass

