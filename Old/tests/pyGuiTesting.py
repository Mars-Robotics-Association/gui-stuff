import dearpygui.dearpygui as dpg
import threading
import time
import requests

xVals = []
yVals = []

series_id = dpg.generate_uuid()
urlBox = dpg.generate_uuid()
checkBox1 = dpg.generate_uuid()
responseLabel = dpg.generate_uuid()

xVal=0;
scanning = 0
keepGoing = 1

def changeScanning():
    global scanning
    scanning = not scanning
    if(scanning==True):
        keepGoing=1
        x = threading.Thread(target=bg_requests, args=(1,))
        x.start()
    else:
        keepGoing=0


requestGood = False
def bg_requests(name):
    while keepGoing==1:
        if scanning==1:
            global requestGood

            requestGood = False
            resp = requests.get(dpg.get_value(urlBox))
            if(resp.status_code==200):
                firstFix = ''.join(resp.text.split('"', 1))
                secondFix = ''.join(firstFix.split('"', 1))
                finalNumber = float(secondFix)

                global xVal
                global xVals
                global yVals
                xVal+=0.5
                xVals.append(xVal)
                yVals.append(finalNumber)
                dpg.set_value(series_id,[xVals,yVals])
                requestGood=True

            else:
                requestGood=False


        time.sleep(0.2)
        if (requestGood):
            dpg.set_value(responseLabel, 'Connection Succeeded')
            dpg.configure_item(responseLabel, color=(0, 255, 0))
        else:
            dpg.set_value(responseLabel, 'Connection Failed')
            dpg.configure_item(responseLabel, color=(255, 0, 0))

with dpg.window(label="Test", height=500, width=500):
    dpg.add_checkbox(label="Collect Data", default_value=False,id=checkBox1,callback=changeScanning)
    dpg.add_text("No Requests Yet",id=responseLabel)
    dpg.add_input_text(label="Robot URL",id=urlBox,default_value="https://api.isaacthoman.me/api/Gui")
    with dpg.plot(label="Plot", height=-1, width=-1) as test_id:
        dpg.add_plot_axis(dpg.mvXAxis, label="x")
        dpg.add_plot_axis(dpg.mvYAxis, label="y")

        dpg.add_line_series(xVals, yVals, label="lineSeries1", parent=dpg.last_item(),id=series_id)

    dpg.plot


dpg.setup_viewport()
dpg.start_dearpygui()
keepGoing=0