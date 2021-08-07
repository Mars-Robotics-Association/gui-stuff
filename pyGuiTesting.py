import dearpygui.dearpygui as dpg
import dearpygui.themes as themes
from dearpygui.logger import mvLogger
from math import sin, cos
import random
import logging
import threading
import time
import requests

xVals = []
yVals = []
url = "https://api.isaacthoman.me/api/Gui" #This would be the URL of the robot's webserver

series_id = dpg.generate_uuid()

xVal=0;
scanning = 1


def bg_requests(name):
    while scanning==1:
        resp = requests.get(url)
        firstFix = ''.join(resp.text.split('"', 1))
        secondFix = ''.join(firstFix.split('"', 1))
        finalNumber = float(secondFix)

        global xVal
        global xVals
        global yVals
        xVal+=0.5
        xVals.append(xVal)
        yVals.append(finalNumber)
        print(finalNumber)

       # dpg.set_item_label(test_id,'hey there')
        dpg.set_value(series_id,[xVals,yVals])
        time.sleep(0.1)


with dpg.window(label="Test", height=500, width=500):
    with dpg.plot(label="Plot", height=-1, width=-1) as test_id:
        dpg.add_plot_axis(dpg.mvXAxis, label="x")
        dpg.add_plot_axis(dpg.mvYAxis, label="y")

        dpg.add_line_series(xVals, yVals, label="lineSeries1", parent=dpg.last_item(),id=series_id)

    dpg.plot

x = threading.Thread(target=bg_requests, args=(1,))
x.start()

#dpg.setup_viewport()
dpg.start_dearpygui()
scanning=0