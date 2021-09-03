import base64
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



#board drawing stuff
with window(label="Game Field", pos=(10, 10)):
    #add_button(label="Move Circle")
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

#image stuff
image_id = 0
defaultImg = b'iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAIAAACRXR/mAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIASURBVFhH7dVfSFNhHMbxV/TGZATBIrbhYIqUYYUQg8Cgm0hQvBBZsE0KMhKiES0kCCG2iHXoz8XUy7roRkTF3QxBFDwg3SUSBG1RKCLRKMhEzIsj7X0gG4b83vd3QOT93p3nvJx9Ls424RzIDIuSYVEyLEqGRelQs9bWVovFYun7T1xrp87aWi/dvXPD6/GIf2s8e34yb+OQaoqskXQCiv/kawrjqFKKrDPeKvnxRzz+m7f6LevZ41Sqp+OyHGU13pM4TU+R1dZ0LHTuUmH1B6531X7hFFxCDDx/g5UYzytfUaAWLFHtx0TMFdbcWBYsIZZ/YyTlCsvZ/AKUELmFjxgpucNytoASYnz+PTZK7rB+fQJKCPvDHl+LfXOFNT8+DJRQfL4rrNBRmILhTkzE+FkXW0JACbG4soGVGANr/evn7q6OSORqa2szOOUGhyZwgh4D6378CiB/q8nZ73BbKQbWg2ud0nKi/nQqY82+XcINjRhY6UREsqL3nmLSjoGVScbASmYwacfAsgZ6Javv4UtM2jGwso9uS1YiPYJJOwbW1OsnkpUdncakHQPLjQ4v69tKse96LBqPzXD8YskYWMflm1UOk3YMD4KoXEHxr7kyBlYdSH/axqYbA8vOjzYEff6Af/DFK0zasb0NvBkWJcOiZFiUDIuSYVE6kCzH2QE4mt54WH8TYQAAAABJRU5ErkJggg=='
helloImg = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAADRSURBVEhL7ZHRDYMwDEQZgREYgREySjZmFEagT7roakhopKqVWinvgx62L+fQ6fgyI6DLCOgyArr8akBKaV3X8nLm0nr/BtN0642txlDOuaiK2IqnsDWvoN1jq6g7JwbbYJ5na4/t+06R1rIsKp7G9NN0gnRdAVt4btumoruESZycRhVW4xSuz1MVcBekXdE9pM11Ooq4mqkDOBTBcDSC9HPal9LWiHiW/6RYtAVwgTQzjU9Ug4FRYXM89A6GtSK8CvgII6DLCOgyArr8e8BxPADpehgpJaleKAAAAABJRU5ErkJggg=='
imageID = generate_uuid()
imageDrawList = generate_uuid()

def baseToImage(imgData):
    global image_id
    with open("imageToSave.png", "wb") as fh:
        fh.write(base64.decodebytes(imgData))

    width, height, channels, data = load_image('imageToSave.png') # 0: width, 1: height, 2: channels, 3: data

    with texture_registry():
        return add_static_texture(width, height, data)


with window(label="Image feed",pos=(735, 10)):

    with drawlist(width=600, height=600,id=imageDrawList):
        newImg = baseToImage(defaultImg)
        newImg2 = baseToImage(helloImg)
        draw_image(newImg, (0, 0), (600, 600),id=imageID)




loop = asyncio.new_event_loop()



async def consumer_handler(websocket) -> None:
    async for message in websocket:
        data = json.loads(message)
        #rp.update(data['xx'], data['yy'])
        print(bytes(data['img'], 'ascii'))
        newImg3 = baseToImage(bytes(data['img'], 'ascii'))

        delete_item(imageDrawList, children_only=True)
        draw_image(newImg3, (0, 0), (600, 600), parent=imageDrawList)


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







