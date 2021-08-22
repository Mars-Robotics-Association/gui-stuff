from dearpygui.dearpygui import *
from random import seed
from random import random
import time

seed(1)
circle_pos = [50,50]
dt=1

def move_circle(sender, app_data, user_data):
    global circle_pos, dt
    
    while dt<10:
        dt+=1
        dx = random()*10*circle_pos[0] % 800
        dy = random()*10*circle_pos[1] % 800
        circle_pos = [dx, dy]
        configure_item(item=get_alias_id("this_circle"), center=circle_pos)
        configure_item(item=get_alias_id("this_circle"), radius=random()*100)
        time.sleep(.1)


with window(label="Tutorial", width=800, height=800):
    add_button(label="Move Circle", callback=move_circle)
    add_drawlist(label="Drawing_1", width=700, height=700)
    draw_circle(label="Drawing_1", center=[0, 0], radius=30, color=[255, 255, 255, 255], id="this_circle")
    print(get_item_configuration(get_alias_id("this_circle")))

print(get_dearpygui_version())
start_dearpygui()
