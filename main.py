import pandas as pd
import numpy
import os

from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn, CheckboxGroup, Button

#init files and direcrions
files = os.listdir('./docs')
directions = []
for file in range(len(files)):
    directions.append([files[file].split()[i] for i in range(len(files[file].split()))])
    directions[file][3] = directions[file][3].replace('.XLS', '')

output_file("index.html")

#init CheckBox
labels = [directions[i][1] for i in range(len(directions))]
checkbox_group = CheckboxGroup(labels=labels)

#init Button
button = Button(label='Сформировать список', button_type = "success")
#button.on_click(updateTable)
#init DataTable

#def updateTable():
#active = [checkbox_group.labels[i] for i in checkbox_group.active]
df = pd.read_excel('./docs/' + files[4], skiprows=5, index_col=0, usecols=[0,1,3,4,5,6,9])

source = ColumnDataSource(df)
columns = [TableColumn(field=df.columns.values[column], title=df.columns.values[column]) for column in range(df.shape[1])]
data_table = DataTable(source = source, columns = columns)

#init show
show(widgetbox(checkbox_group))
show(widgetbox(button))
show(widgetbox(data_table))
