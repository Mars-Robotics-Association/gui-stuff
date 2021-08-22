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
robotHeight = 150

givenCenter = [250,250]
givenRotation = 45



def move_polygon(sender, app_data, user_data):
    while(1==1):
        global polyPointsX,polyPointsY,givenCenter,givenRotation
        givenRotation+=0.1

        firstX = givenCenter[0]
        firstY = givenCenter[1]

        secondX = firstX + robotHeight * math.cos(givenRotation+90 * math.pi / 180)
        secondY = firstY + robotHeight * math.sin(givenRotation+90 * math.pi / 180)

        thirdX = secondX + robotWidth * math.cos(givenRotation+180 * math.pi / 180)
        thirdY = secondY + robotWidth * math.sin(givenRotation+180 * math.pi / 180)

        fourthX = thirdX + robotHeight * math.cos(givenRotation + 270 * math.pi / 180)
        fourthY = thirdY + robotHeight * math.sin(givenRotation + 270 * math.pi / 180)

        #x + distance * math.cos(angle_degrees * math.pi / 180)


        configure_item(item=get_alias_id("this_polygon"), points=((firstX,firstY),(secondX,secondY),(thirdX,thirdY),(fourthX,fourthY)))
        time.sleep(0.01)



with window(label="Tutorial", width=800, height=800):
    add_button(label="Move Circle", callback=move_polygon)
    add_drawlist(label="Drawing_1", width=700, height=700)

    draw_polygon(label="Drawing_2", points=((50,50),(50,100),(100,100),(100,50),(50,50)),  fill=[255, 255, 255], id="this_polygon")

print(get_dearpygui_version())
start_dearpygui()