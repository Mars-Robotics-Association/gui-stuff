import asyncio
import websockets
import logging
import dearpygui.dearpygui as dpg
import threading
import time
import requests
import math

with dpg.window(label="Test", height=500, width=500):
    dpg.add_checkbox(label="Collect Data", default_value=False)
    dpg.add_text("No Requests Yet")
    dpg.add_input_text(label="Robot URL", default_value="default value")
    with dpg.plot(label="Plot", height=-1, width=-1) as test_id:
        dpg.add_plot_axis(dpg.mvXAxis, label="x")
        dpg.add_plot_axis(dpg.mvYAxis, label="y")

        dpg.add_line_series([0, 1], [0, 1], label="lineSeries1", parent=dpg.last_item())

    dpg.plot


def showPyGui():
    dpg.setup_viewport()
    dpg.start_dearpygui()


x = threading.Thread(target=showPyGui(), args=(1,))
x.start()


# below is websocket stuff
async def consumer_handler(websocket) -> None:
    async for message in websocket:
        print("got message!")
        print(message)


async def consume(hostname: str, port: int) -> None:
    websocket_resource_url = f"ws://{hostname}:{port}"
    async with websockets.connect(websocket_resource_url, ping_interval=5) as websocket:
        await consumer_handler(websocket)


if __name__ == '__main__':
    # logger = logging.getLogger('websockets')
    # logger.setLevel(logging.DEBUG)
    # logger.addHandler(logging.StreamHandler())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume(hostname="localhost", port=8765))
    loop.run_forever()

