import pandas as pd
import numpy
import os

from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import DataTable, TableColumn, CheckboxGroup, Button
from bokeh.plotting import curdoc


files = os.listdir('./docs')
directions = []
for file in range(len(files)):
    directions.append([files[file].split()[i] for i in range(len(files[file].split()))])
    #files.insert(file, [files[file].split()[i] for i in range(len(files[file].split()))])
    directions[file][3] = directions[file][3].replace('.XLS', '')
  
output_file("index.html")

labels = [directions[i][1] for i in range(len(directions))]
checkbox_group = CheckboxGroup(labels=labels, active=[0,1])
#init function for upgrade
#active = [checkbox_group.labels[i] for i in checkbox_group.active]

def updateTable():
    #global active
    act = [checkbox_group.labels[i] for i in checkbox_group.active]
    return CustomJS(args=dict(), code=open('./updateTable.js').read())

checkbox_group.js_on_change('active', updateTable())

button = Button(label='Сформировать список', button_type = "success")
#button.callback = CustomJS(args=dict(active=act),code=open('./updateTable.js').read())

#init DataTable
#initial_carriers = checkbox_group.labels[i] for i in checkbox_group.active]
#df1 = pd.read_excel('./docs/' + files[4], skiprows=5, index_col=0)

#df2 = pd.read_excel('./docs/' + files[3], skiprows=5, index_col=0)

#df3  = df2.merge(df1, how='outer')
layout = widgetbox(button, checkbox_group)
#chbg = widgetbox(checkbox_group)
#curdoc().add_root(layout)
show(layout)
#bokeh serve --show files\test.py