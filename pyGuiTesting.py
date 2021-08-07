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


xVal=0;
scanning = 1
def bg_requests(name):
    while scanning==1:
        resp = requests.get(url)
        firstFix = ''.join(resp.text.split('"', 1))
        secondFix = ''.join(firstFix.split('"', 1))
        finalNumber = float(secondFix)
        print(finalNumber)
        time.sleep(5)
        global xVal
        global xVals
        global yVals
        xVal+=1
        xVals.append(xVal)
        yVals.append(finalNumber)
        #would want to update the plot here, need to figure that out





with dpg.window(label="Test"):
    with dpg.plot(label="Plot", height=500, width=500):
        dpg.add_plot_axis(dpg.mvXAxis, label="x")
        dpg.add_plot_axis(dpg.mvYAxis, label="y")

        dpg.add_line_series(xVals, yVals, label="label", parent=dpg.last_item())
    dpg.plot

x = threading.Thread(target=bg_requests, args=(1,))
x.start()

dpg.setup_viewport()
dpg.start_dearpygui()
scanning=0
