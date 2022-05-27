import base64
import dearpygui.dearpygui as dpg
from dearpygui.dearpygui import *

exampleBase64 = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAIAAAD8GO2jAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAADRSURBVEhL7ZHRDYMwDEQZgREYgREySjZmFEagT7roakhopKqVWinvgx62L+fQ6fgyI6DLCOgyArr8akBKaV3X8nLm0nr/BtN0642txlDOuaiK2IqnsDWvoN1jq6g7JwbbYJ5na4/t+06R1rIsKp7G9NN0gnRdAVt4btumoruESZycRhVW4xSuz1MVcBekXdE9pM11Ooq4mqkDOBTBcDSC9HPal9LWiHiW/6RYtAVwgTQzjU9Ug4FRYXM89A6GtSK8CvgII6DLCOgyArr8e8BxPADpehgpJaleKAAAAABJRU5ErkJggg=='

# Converts base 64 to Image object
def baseToImage(imgData):
    global image_id
    with open("imageToSave.png", "wb") as fh:
        fh.write(base64.decodebytes(imgData))

    width, height, channels, data = load_image('imageToSave.png') # 0: width, 1: height, 2: channels, 3: data

    with texture_registry():
        return add_static_texture(width, height, data)

def getImage():
    return exampleBase64

def save_callback():
    print("Save Clicked")

def show():
    image = baseToImage(getImage())
    with dpg.window(label="OpenCV Image Stream"):
        dpg.add_image(image)
        dpg.add_text("Click to save image to ...")
        dpg.add_input_text(label="Save image name")
        dpg.add_button(label="Save", callback=save_callback)
