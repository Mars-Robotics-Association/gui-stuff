import dearpygui.dearpygui as dpg
import threading
import base64
imageID = dpg.generate_uuid()

img_data = 'hey'
with open("imageToSave.png", "wb") as fh:
    fh.write(base64.decodebytes(img_data))

width, height, channels, data = dpg.load_image('imageToSave.png') # 0: width, 1: height, 2: channels, 3: data

with dpg.texture_registry():
    image_id = dpg.add_static_texture(width, height, data)

with dpg.window(label="Tutorial"):

    with dpg.drawlist(width=650, height=770):
        dpg.draw_image(image_id, (0, 0), (600, 600), uv_min=(0, 0), uv_max=(1, 1),id=imageID)


dpg.start_dearpygui()