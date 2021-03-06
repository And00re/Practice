import pandas as pd
import numpy as np
import os
from os.path import dirname, join 

from bokeh.layouts import widgetbox, row
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import DataTable, TableColumn, CheckboxGroup, Button
from bokeh.io import curdoc

files = os.listdir(join(dirname(__file__), 'docs'))
directions = []
for file in range(len(files)):
    directions.append([files[file].split()[i] for i in range(len(files[file].split()))])
    directions[file][-1] = directions[file][-1].replace('.XLS', '')

def update(attr, old, new):
    #act = [checkbox_group.labels[i] for i in checkbox_group.active]
    df_new = df_initial
    for i in checkbox_group.active:
        df = pd.read_excel(join(dirname(__file__), 'docs', files[i]), skiprows=5, usecols=[0,1,3,4,5,6,9])
        df[df.columns.values[6]] = df[df.columns.values[6]].fillna('')
        for line in df[df.columns.values[6]].index:
            if df.loc[line,df.columns.values[6]] != '':
                df.loc[line, df.columns.values[6]] = directions[i][1]
        df_new = pd.merge(df_new, df,
                          how='outer',
                          on=df.columns.values.tolist())
        df_new = df_new.sort_values(by = df_new.columns.values[6], ascending=False)
        df_new = df_new.drop_duplicates(df.columns.values[1], keep='first')
        df_new = df_new.sort_values(by = df_new.columns.values[0])
    df_new.drop(df_new.columns.values[0], axis=1, inplace = True)
    source.data = {df_new.columns.values[column] : df_new[df_new.columns.values[column]] for column in range(df_new.shape[1])}

labels = [' '.join(directions[i]) for i in range(len(directions))]
checkbox_group = CheckboxGroup(labels=labels)
checkbox_group.on_change('active', update)

df_initial = pd.read_excel(join(dirname(__file__), 'docs', files[0]), skiprows=5, usecols=[0,1,3,4,5,6,9], nrows=0) 
source = ColumnDataSource(data = dict())
columns = [TableColumn(field=df_initial.columns.values[column], title=df_initial.columns.values[column]) for column in range(1, df_initial.shape[1])]
data_table = DataTable(source=source, columns=columns, width=1000, height=2000)
'''
df_new = df_initial
for i in range(2):
    df = pd.read_excel(join(dirname(__file__), 'docs', files[i]), skiprows=5, usecols=[0,1,3,4,5,6,9])
    df[df.columns.values[6]] = df[df.columns.values[6]].fillna('')
    for line in df[df.columns.values[6]].index:
        if df.loc[line,df.columns.values[6]] != '':
            df.loc[line, df.columns.values[6]] = directions[i][1]
    df_new = pd.merge(df_new, df, how='outer', on=df.columns.values.tolist())
    df_new = df_new.sort_values(by = df_new.columns.values[6], ascending=False)
    df_new = df_new.drop_duplicates(df.columns.values[1], keep='first')
    df_new = df_new.sort_values(by = df_new.columns.values[0])
df_new = df_new.drop(df_new.columns.values[0], axis=1)
print(df_new)
'''
control = widgetbox(checkbox_group)
table = widgetbox(data_table)

curdoc().add_root(row(control,table))

#bokeh serve --show files\test.py