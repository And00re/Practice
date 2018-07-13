import pandas as pd
import numpy
import os

from bokeh.layouts import widgetbox, row
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import DataTable, TableColumn, CheckboxGroup, Button
from bokeh.io import curdoc

files = os.listdir('./docs')
directions = []
for file in range(len(files)):
    directions.append([files[file].split()[i] for i in range(len(files[file].split()))])
    directions[file][3] = directions[file][3].replace('.XLS', '')

df = pd.read_excel('./docs/' + files[0], skiprows=5, index_col=0, usecols=[0,1,3,4,5,6,9]) 
source = ColumnDataSource(data = dict())

def make_Table(df):
    source = ColumnDataSource(df)
    columns = [TableColumn(field=df.columns.values[column], title=df.columns.values[column]) for column in range(df.shape[1])]
    return DataTable(source=source, columns=columns)

def update(attr, old, new):
    #act = [checkbox_group.labels[i] for i in checkbox_group.active]
    for i in checkbox_group.active:
       df = pd.read_excel('./docs/' + files[i], skiprows=5, index_col=0, usecols=[0,1,3,4,5,6,9]) 
    source.data = {df.columns.values[column] : df[df.columns.values[column]] for column in range(df.shape[1])}

#def form():
#   source = ColumnDataSource(df)
#   data_table = DataTable(source=source, columns=columns)

labels = [directions[i][1] for i in range(len(directions))]
checkbox_group = CheckboxGroup(labels=labels)
checkbox_group.on_change('active', update)

#button = Button(label='Сформировать список', button_type = "success")
#button.on_click(update)
#button.callback = CustomJS(args=dict(active=act),code=open('./updateTable.js').read())
#initial_carriers = [checkbox_group.labels[i] for i in checkbox_group.active]

columns = [TableColumn(field=df.columns.values[column], title=df.columns.values[column]) for column in range(df.shape[1])]
data_table = DataTable(source=source, columns=columns, width=800)

#init DataTable
#initial_carriers = checkbox_group.labels[i] for i in checkbox_group.active]
#df1 = pd.read_excel('./docs/' + files[4], skiprows=5, index_col=0)

#df2 = pd.read_excel('./docs/' + files[3], skiprows=5, index_col=0)

#df3  = df2.merge(df1, how='outer')

control = widgetbox(checkbox_group)
table = widgetbox(data_table)

curdoc().add_root(row(control,table))

#bokeh serve --show files\test.py
update