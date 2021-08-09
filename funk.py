import dearpygui.dearpygui as dpg
import threading
import time
import requests
import math
me = dpg.generate_uuid()
testLayer1 = dpg.generate_uuid()

circleX=200
circleY=200
requestGood = False
xDir = 1
yDir = 1

carX = 300
carY = 300
width = 50
height = 50
angle = 20
accelForward = 1
accelRotation = -3

def bg_requests(name):
    while 1==1:
        global circleX, circleY, xDir, yDir, carX, carY, width, height, angle, accelForward, accelRotation
        if dpg.is_key_down(87):
            accelForward += 0.3
        if dpg.is_key_down(83):
            accelForward += -0.3
        if dpg.is_key_down(65):
            accelRotation += 0.3
        if dpg.is_key_down(68):
            accelRotation += -0.3

        if accelForward > 0:
            accelForward -= 0.1
        if accelForward < 0:
            accelForward += 0.1
        if accelRotation > 0:
            accelRotation -= 0.1
        if accelRotation < 0:
            accelRotation += 0.1

        if accelForward > 5:
            accelForward = 5
        if accelForward < -5:
            accelForward = -5
        if accelRotation > 5:
            accelRotation = 5
        if accelRotation < -5:
            accelRotation = -5

        if math.fabs(accelForward) < 0.1:
            accelForward = 0
        if math.fabs(accelRotation) < 0.1:
            accelRotation = 0

        carX += math.sin(angle / 180 * 3.14) * accelForward
        carY += math.cos(angle / 180 * 3.14) * accelForward
        angle += accelRotation

        dpg.delete_item(testLayer1, children_only=True)

        pointA = [math.sin((45 + angle) / 180 * 3.14) * width + carX, math.cos((45 + angle) / 180 * 3.14) * height + carY]
        pointB = [math.sin((135 + angle) / 180 * 3.14) * width + carX, math.cos((135 + angle) / 180 * 3.14) * height + carY]
        pointC = [math.sin((225 + angle) / 180 * 3.14) * width + carX, math.cos((225 + angle) / 180 * 3.14) * height + carY]
        pointD = [math.sin((315 + angle) / 180 * 3.14) * width + carX, math.cos((315 + angle) / 180 * 3.14) * height + carY]

        dpg.draw_rectangle([0, 0], [800, 500], parent=testLayer1, fill=(50, 50, 50))
        dpg.draw_polygon([pointA, pointB, pointC, pointD, pointA], parent=testLayer1, fill=(255, 0, 255))


        time.sleep(0.01)

draw_thickness = 5
draw_size = 5
draw_color = 5
draw_spacing = 5
draw_rounding = 5
with dpg.window(label="I hate jazz.", height=750, width=850):
    dpg.add_text("I hate Mike Krol.")
    with dpg.drawlist(width=800, height=500,id=me):
        dpg.add_draw_layer(id=testLayer1)
        #dpg.draw_circle([150, 150], 50, thickness=50, color=(255,0,255))


x = threading.Thread(target=bg_requests, args=(1,))
x.start()

dpg.setup_viewport()
dpg.start_dearpygui()