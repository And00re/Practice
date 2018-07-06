import pandas as pd
import numpy

from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import DataTable, TableColumn

df = pd.read_excel('09.03.02 ИСиТ О Б.XLS', skiprows=5, index_col=0)
df.index.name = 'index'

output_file("index.html")

source = ColumnDataSource(df)

columns = [TableColumn(field=df.columns.values[column], title=df.columns.values[column]) for column in range(df.shape[1])]

data_table = DataTable(source = source, columns = columns)

show(widgetbox(data_table))