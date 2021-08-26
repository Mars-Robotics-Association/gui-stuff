import time

from dearpygui.dearpygui import *
from random import seed
import math

seed(1)
circle_pos = [50,50]
dt=1
polyPointsX = [0,0,50,50]
polyPointsY = [0,50,50,0]

robotWidth = 100
robotHeight = 120

givenCenter = [250,250]
givenRotation = 45



def move_polygon(sender, app_data, user_data):
    while(1==1):
        global polyPointsX,polyPointsY,givenCenter,givenRotation
        givenRotation+=2
        xVals = []
        yVals = []

        xVals.append(givenCenter[0] + ((robotWidth / 2) * math.cos(givenRotation*3.14/180)) - ((robotHeight / 2) * math.sin(givenRotation*3.14/180)))
        yVals.append(givenCenter[1] + ((robotWidth / 2) * math.sin(givenRotation*3.14/180)) + ((robotHeight / 2) * math.cos(givenRotation*3.14/180)))

        xVals.append(givenCenter[0] - ((robotWidth / 2) * math.cos(givenRotation*3.14/180)) - ((robotHeight / 2) * math.sin(givenRotation*3.14/180)))
        yVals.append(givenCenter[1] - ((robotWidth / 2) * math.sin(givenRotation*3.14/180)) + ((robotHeight / 2) * math.cos(givenRotation*3.14/180)))

        xVals.append(givenCenter[0] - ((robotWidth / 2) * math.cos(givenRotation*3.14/180)) + ((robotHeight / 2) * math.sin(givenRotation*3.14/180)))
        yVals.append(givenCenter[1] - ((robotWidth / 2) * math.sin(givenRotation*3.14/180)) - ((robotHeight / 2) * math.cos(givenRotation*3.14/180)))

        xVals.append(givenCenter[0] + ((robotWidth / 2) * math.cos(givenRotation*3.14/180)) + ((robotHeight / 2) * math.sin(givenRotation*3.14/180)))
        yVals.append(givenCenter[1] + ((robotWidth / 2) * math.sin(givenRotation*3.14/180)) - ((robotHeight / 2) * math.cos(givenRotation*3.14/180)))

        #x + distance * math.cos(angle_degrees * math.pi / 180)


        configure_item(item=get_alias_id("this_polygon"), points=((xVals[0],yVals[0]),(xVals[1],yVals[1]),(xVals[2],yVals[2]),(xVals[3],yVals[3]),(xVals[0],yVals[0])))
        time.sleep(0.01)



with window(label="Tutorial", width=800, height=800):
    add_button(label="Move Circle", callback=move_polygon)
    with drawlist(label="Drawing_1", width=700, height=700,id="drawlist"):

        draw_rectangle((0,0),(700,700),fill=(150,150,150))

        squareLength = get_item_width('drawlist')/8
        for xLine in range(8):
            if(xLine != 0):
                draw_line((squareLength*xLine,0),(squareLength*xLine,squareLength*8),color=(100,100,100))
        for xLine in range(8):
            if(xLine != 0):
                draw_line((0,squareLength*xLine),(squareLength*8,squareLength*xLine),color=(100,100,100))
        draw_polygon(label="Drawing_2", points=((50,50),(50,100),(100,100),(100,50),(50,50)),  fill=[100, 255, 120], id="this_polygon")

print(get_dearpygui_version())
start_dearpygui()
