from motionDetection import obj_Det
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

obj_Det["Start_string"] = obj_Det["Start Time"].dt.strftime("%Y-%m-%d %H:%M:%S")
obj_Det["End_string"] = obj_Det["End Time"].dt.strftime("%Y-%m-%d %H:%M:%S")
colDatSor=ColumnDataSource(obj_Det)

p= figure(x_axis_type = 'datetime', height=100, width=500, sizing_mode="scale_both", title="Motion Detection Graph")
p.yaxis.minor_tick_line_color=None
p.yaxis[0].ticker.desired_num_ticks = 1


hover= HoverTool(tooltips=[("Start Time ", "@Start_string"), ("End Time ", "@End_string")])
p.add_tools(hover)

q=p.quad(left="Start Time", right="End Time", bottom=0, top=1, color="orange", source=colDatSor)

output_file("MotionDetGraph1.html")
show(p)