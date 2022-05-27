from random import Random, random, randrange
import threading
import dearpygui.dearpygui as dpg
from robotPose import RobotPositionMap
import openCVStream
import random



def save_callback():
    print("Save Clicked")



dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

# robotCircle = dpg.generate_uuid()
# robotIcon = dpg.generate_uuid()

# class RobotPosition:
#     def __init__(self):
#         self.xx = 0
#         self.yy = 0
#         self._lock = threading.Lock()

#     #updates the robot's position on the field
#     def update(self, newx, newy):
#         print(newx, newy)
#         with self._lock:
#             self.xx = newx
#             self.yy = newy
#             dpg.delete_item(robotIcon, children_only=True)
#             dpg.draw_circle([self.xx, self.yy], 50, thickness=10, color=(255, 0, 255), parent=robotIcon, id=robotCircle)

openCVStream.show()

robotPos = RobotPositionMap()
robotPos.drawField()

#board drawing stuff
# with dpg.window(label="Game Field", pos=(10, 10)):
#     #add_button(label="Move Circle")
#     with dpg.drawlist(label="Drawing_1", width=700, height=700,id="drawlist"):

#         dpg.draw_rectangle((0,0),(700,700),fill=(150,150,150))

#         squareLength = dpg.get_item_width('drawlist')/6
#         for xLine in range(6):
#             if(xLine != 0):
#                 dpg.draw_line((squareLength*xLine,0),(squareLength*xLine,squareLength*6),color=(100,100,100))
#         for xLine in range(6):
#             if(xLine != 0):
#                 dpg.draw_line((0,squareLength*xLine),(squareLength*6,squareLength*xLine),color=(100,100,100))
#         dpg.draw_polygon(label="Drawing_2", points=((50,50),(50,100),(100,100),(100,50),(50,50)),  fill=[100, 255, 120], id="this_polygon")

# with dpg.window(label="Window", height=750, width=850):
#     with dpg.drawlist(width=800, height=500,id=robotIcon, callback=save_callback):
#         newCircle = dpg.draw_circle([150, 150], 50, thickness=10, color=(255,0,255), id=robotCircle,label="myCircle")
#         dpg.configure_item(newCircle, center=[150,450])

dpg.show_viewport()

# below replaces, start_dearpygui()
while dpg.is_dearpygui_running():
    # insert here any code you would like to run in the render loop
    # you can manually stop by using stop_dearpygui()
    robotPos.update(random.randrange(0,800,1), random.randrange(0,800,1)) #randomize robot's pose
    dpg.render_dearpygui_frame()

dpg.destroy_context()