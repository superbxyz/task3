import csv
import serial
import datetime
from serial import SerialException
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Div
from bokeh.layouts import column
from bokeh.models import HoverTool
# Using hover tool
hover_tool = HoverTool(tooltips=[("time", "@time"), ("distance", "@distance")])
p = figure(x_axis_type='datetime', y_axis_label='distance', sizing_mode='stretch_width')
p.add_tools(hover_tool)
# naming x axis and y axis
source = ColumnDataSource(data=dict(time=[], distance=[]))
p.line(x='time', y='distance', line_width=2, source=source)
# to display the popup message in graph 
message_text = Div(text="", width=200, height=100)
#for reading the port which is connected with baud rate 9600.
try:
    ser = serial.Serial('COM10', 9600)
except SerialException:
    message_text.text = "The port is not detected."#to display port is not detected in the graph and terminal.
    print("Port is disconnected.")
#to save the data printed in the teminal to a csv file with time.
csv_filename = 'port.csv'
csv_file = open(csv_filename, 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Time', 'distance'])

def update_data():
    try:
        data = ser.readline().decode().strip()
        time = datetime.datetime.now()
        distance = float(data)

        new_data = dict(time=[time], distance=[distance])
        source.stream(new_data, rollover=100)

        csv_writer.writerow([time, distance])
        csv_file.flush()

        print(f"Time: {time}, distance: {distance}")

        message_text.text = ""
    except SerialException:
        message_text.text = "The port is disconnected." 
        print("Port is disconnected.")
    except KeyboardInterrupt:
        message_text.text = "manually stopped printing data"
        print("manually stopped printing data") # to display stop printing data when ctrl+c is pressed.

#to change the title size, align the text to the center, move it to the right, change its color to red, and set the font to bold
title_div = "<div style='font-size: 20pt; text-align: center; margin-left: 50px; color: red; font-weight: bold;'>TEAM ASSAILING FALCONS</div>"

layout = column(Div(text=title_div), p, message_text, width=800, height=400, sizing_mode='scale_width')

curdoc().add_periodic_callback(update_data, 1000)

curdoc().title = "Real-time Serial Plot"
curdoc().add_root(layout)
