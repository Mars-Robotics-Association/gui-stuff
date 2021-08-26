import time
from dearpygui.dearpygui import *
from random import seed
import math
import threading,asyncio,websockets,json

seed(1)
circle_pos = [50,50]
dt=1
polyPointsX = [0,0,50,50]
polyPointsY = [0,50,50,0]

robotWidth = 100
robotHeight = 120
givenCenter = [250,250]
givenRotation = 45
demoRadius = 200
demoRadiusChange = 1

def move_polygon(givenCenterX, givenCenterY, givenRotation):

    global polyPointsX,polyPointsY,demoRadius,demoRadiusChange
    #givenRotation+=2

    #givenCenter[0] = 700 / 2 + demoRadius * math.cos(givenRotation * math.pi / 180)
    #givenCenter[1] = 700 / 2 + demoRadius * math.sin(givenRotation * math.pi / 180)

    xVals = []
    yVals = []

    xVals.append(givenCenterX + ((robotWidth / 2) * math.cos(givenRotation*3.14/180)) - ((robotHeight / 2) * math.sin(givenRotation*3.14/180)))
    yVals.append(givenCenterY + ((robotWidth / 2) * math.sin(givenRotation*3.14/180)) + ((robotHeight / 2) * math.cos(givenRotation*3.14/180)))

    xVals.append(givenCenterX - ((robotWidth / 2) * math.cos(givenRotation*3.14/180)) - ((robotHeight / 2) * math.sin(givenRotation*3.14/180)))
    yVals.append(givenCenterY - ((robotWidth / 2) * math.sin(givenRotation*3.14/180)) + ((robotHeight / 2) * math.cos(givenRotation*3.14/180)))

    xVals.append(givenCenterX - ((robotWidth / 2) * math.cos(givenRotation*3.14/180)) + ((robotHeight / 2) * math.sin(givenRotation*3.14/180)))
    yVals.append(givenCenterY - ((robotWidth / 2) * math.sin(givenRotation*3.14/180)) - ((robotHeight / 2) * math.cos(givenRotation*3.14/180)))

    xVals.append(givenCenterX + ((robotWidth / 2) * math.cos(givenRotation*3.14/180)) + ((robotHeight / 2) * math.sin(givenRotation*3.14/180)))
    yVals.append(givenCenterY + ((robotWidth / 2) * math.sin(givenRotation*3.14/180)) - ((robotHeight / 2) * math.cos(givenRotation*3.14/180)))

    #x + distance * math.cos(angle_degrees * math.pi / 180)


    configure_item(item=get_alias_id("this_polygon"), points=((xVals[0],yVals[0]),(xVals[1],yVals[1]),(xVals[2],yVals[2]),(xVals[3],yVals[3]),(xVals[0],yVals[0])))




with window(label="Tutorial", width=800, height=800):
    add_button(label="Move Circle")
    with drawlist(label="Drawing_1", width=700, height=700,id="drawlist"):

        draw_rectangle((0,0),(700,700),fill=(150,150,150))

        squareLength = get_item_width('drawlist')/6
        for xLine in range(6):
            if(xLine != 0):
                draw_line((squareLength*xLine,0),(squareLength*xLine,squareLength*6),color=(100,100,100))
        for xLine in range(6):
            if(xLine != 0):
                draw_line((0,squareLength*xLine),(squareLength*6,squareLength*xLine),color=(100,100,100))
        draw_polygon(label="Drawing_2", points=((50,50),(50,100),(100,100),(100,50),(50,50)),  fill=[100, 255, 120], id="this_polygon")

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
        print(data['img'])
        move_polygon(data['xx']*700,data['yy']*700,data['hh']*700)

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


print(get_dearpygui_version())
start_dearpygui()


print("EXITED DEAR PY GUI")
try:
    for task in asyncio.all_tasks(loop):
        task.cancel()
except asyncio.CancelledError:
    pass







