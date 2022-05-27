from random import Random, random, randrange
import threading
import dearpygui.dearpygui as dpg
import openCVStream
import random

class RobotPositionMap:

    dpg.create_context()
    robotCircle = 0
    robotIcon = 1

    def __init__(self):
        self.xx = 0
        self.yy = 0
        self._lock = threading.Lock()
        

    def drawField(self):
        print("Drawing Field...")
        self.robotCircle = dpg.generate_uuid()
        self.robotIcon = dpg.generate_uuid()
        #board drawing stuff
        with dpg.window(label="Game Field", pos=(10, 10)):
            #draws the field
            with dpg.drawlist(label="Field", width=700, height=700,tag="drawlist"):
                dpg.draw_rectangle((0,0),(700,700),fill=(150,150,150)) #draws background
                squareLength = dpg.get_item_width('drawlist')/6 
                for xLine in range(6):
                    if(xLine != 0):
                        dpg.draw_line((squareLength*xLine,0),(squareLength*xLine,squareLength*6),color=(100,100,100))
                for xLine in range(6):
                    if(xLine != 0):
                        dpg.draw_line((0,squareLength*xLine),(squareLength*6,squareLength*xLine),color=(100,100,100))

                #draws robot
                robot = dpg.draw_circle([150, 150], 50, thickness=10, color=(255,0,255), tag=self.robotCircle,label="robot")
                dpg.configure_item(robot, center=[150,450])    

    #updates the robot's position on the field
    def update(self, newx, newy):
        print(newx, newy)
        with self._lock:
            self.xx = newx
            self.yy = newy
            dpg.delete_item(self.robotIcon, children_only=True)
            dpg.draw_circle([self.xx, self.yy], 50, thickness=10, color=(255, 0, 255), parent=self.robotIcon, tag=self.robotCircle)