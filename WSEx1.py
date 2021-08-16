
import asyncio
import websockets
import time

async def hello(websocket, path):

    await websocket.send("hey")
    print(f"done")
    time.sleep(1)

start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()