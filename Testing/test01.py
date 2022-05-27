import dearpygui.dearpygui as dpg



def save_callback():

    print("Save Clicked")



dpg.create_context()

dpg.create_viewport()

dpg.setup_dearpygui()



#board drawing stuff
with dpg.window(label="Game Field", pos=(10, 10)):
    #add_button(label="Move Circle")
    with dpg.drawlist(label="Drawing_1", width=700, height=700,id="drawlist"):

        dpg.draw_rectangle((0,0),(700,700),fill=(150,150,150))

        squareLength = dpg.get_item_width('drawlist')/6
        for xLine in range(6):
            if(xLine != 0):
                dpg.draw_line((squareLength*xLine,0),(squareLength*xLine,squareLength*6),color=(100,100,100))
        for xLine in range(6):
            if(xLine != 0):
                dpg.draw_line((0,squareLength*xLine),(squareLength*6,squareLength*xLine),color=(100,100,100))
        dpg.draw_polygon(label="Drawing_2", points=((50,50),(50,100),(100,100),(100,50),(50,50)),  fill=[100, 255, 120], id="this_polygon")



dpg.show_viewport()

dpg.start_dearpygui()

dpg.destroy_context()