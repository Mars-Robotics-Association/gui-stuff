import dearpygui.dearpygui as dpg
import threading
import time
import requests
me = dpg.generate_uuid()

circleX=200
circleY=200
requestGood = False
xDir = 1
yDir = 1


def bg_requests(name):
    while 1==1:
        global circleX
        global circleY
        global isWDown
        global xDir
        global yDir

        circleX+=xDir
        circleY+=yDir

        dpg.set_value(me,[circleX,circleY])
        dpg.draw_rectangle([0,0],[50000,50000],parent=me,fill=(50,50,50))
        dpg.draw_circle([circleX, circleY], 50, thickness=10, color=(255, 0, 255),parent=me)

        if (circleX > 800 - 50):
            xDir = -1
        if (circleY > 500 - 50):
            yDir = -1
        if (circleX < 50):
            xDir = 1
        if (circleY < 50):
            yDir = 1


        time.sleep(0.01)

draw_thickness = 5
draw_size = 5
draw_color = 5
draw_spacing = 5
draw_rounding = 5
with dpg.window(label="I hate jazz.", height=750, width=850):
    dpg.add_text("I hate Mike Krol.")
    with dpg.drawlist(width=800, height=500,id=me):
        dpg.draw_circle([150, 150], 50, thickness=50, color=(255,0,255))


x = threading.Thread(target=bg_requests, args=(1,))
x.start()

dpg.setup_viewport()
dpg.start_dearpygui()