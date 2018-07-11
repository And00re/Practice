import pandas as pd
import numpy
import os

from bokeh.io import output_file, show, curdoc
from bokeh.layouts import widgetbox, row
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import DataTable, TableColumn, CheckboxGroup, Button

files = os.listdir('./docs')
directions = []
for file in range(len(files)):
    directions.append([files[file].split()[i] for i in range(len(files[file].split()))])
    #files.insert(file, [files[file].split()[i] for i in range(len(files[file].split()))])
    directions[file][3] = directions[file][3].replace('.XLS', '')
  
#output_file("index.html")

df = pd.read_excel('./docs/' + files[0], skiprows=5, index_col=0, usecols=[0,1,3,4,5,6,9]) 

def make_Table(df):
    source = ColumnDataSource(df)
    print(source.data)
    columns = [TableColumn(field=df.columns.values[column], title=df.columns.values[column]) for column in range(df.shape[1])]
    return DataTable(source=source, columns=columns)

def update():
    #act = [checkbox_group.labels[i] for i in checkbox_group.active]
    for i in checkbox_group.active:
        df = pd.read_excel('./docs/' + files[i], skiprows=5, index_col=0, usecols=[0,1,3,4,5,6,9]) 

    #return CustomJS(args=dict(), code=open('./updateTable.js').read())

#def form():
#    source = ColumnDataSource(df)
#   data_table = DataTable(source=source, columns=columns)

labels = [directions[i][1] for i in range(len(directions))]
checkbox_group = CheckboxGroup(labels=labels)
checkbox_group.on_change('active', lambda attr, old, new: update())

button = Button(label='Сформировать список', button_type = "success")
#button.callback = CustomJS(args=dict(active=act),code=open('./updateTable.js').read())
#button.on_click(form)
#initial_carriers = [checkbox_group.labels[i] for i in checkbox_group.active]
source = ColumnDataSource(df)
columns = [TableColumn(field=df.columns.values[column], title=df.columns.values[column]) for column in range(df.shape[1])]
data_table = make_Table(df)
#init DataTable
#initial_carriers = checkbox_group.labels[i] for i in checkbox_group.active]
#df1 = pd.read_excel('./docs/' + files[4], skiprows=5, index_col=0)

#df2 = pd.read_excel('./docs/' + files[3], skiprows=5, index_col=0)

#df3  = df2.merge(df1, how='outer')

control = widgetbox(button, checkbox_group)
table = widgetbox(data_table)
curdoc().add_root(row(control,table))

#show(layout)
#bokeh serve --show files\test.py
#update()