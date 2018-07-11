from os.path import dirname, join

import pandas as pd

from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import RangeSlider, Button, DataTable, TableColumn, NumberFormatter
from bokeh.io import curdoc

df = pd.read_csv('./files/salary_data.csv')

source = ColumnDataSource(data=dict())

def update():
    current = df[(df['salary'] >= slider.value[0]) & (df['salary'] <= slider.value[1])].dropna()
    source.data = {
        'name'             : current.name,
        'salary'           : current.salary,
        'years_experience' : current.years_experience,
    }

slider = RangeSlider(title="Max Salary", start=10000, end=110000, value=(10000, 50000), step=1000, format="0,0")
slider.on_change('value', lambda attr, old, new: update())

columns = [
    TableColumn(field="name", title="Employee Name"),
    TableColumn(field="salary", title="Income", formatter=NumberFormatter(format="$0,0.00")),
    TableColumn(field="years_experience", title="Experience (years)")
]

data_table = DataTable(source=source, columns=columns, width=800)

controls = widgetbox(slider)
table = widgetbox(data_table)

curdoc().add_root(row(controls, table))
curdoc().title = "Export CSV"

update()
#bokeh serve --show files\test\test5.py