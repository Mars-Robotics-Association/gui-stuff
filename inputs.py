import time

from dearpygui.dearpygui import *
from random import seed
import math


with window(label="Tutorial", width=800, height=800):
    for test in range(10):
        add_collapsing_header(label=test, parent=test, id=test + 1)

print(get_dearpygui_version())
start_dearpygui()

