import pandas as pd
import numpy as np
import os
from os.path import dirname, join
import collections 
from jinja2 import Environment, FileSystemLoader
from tornado.web import RequestHandler
from tornado.ioloop import IOLoop

from bokeh.layouts import widgetbox, row, column, layout
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import DataTable, TableColumn, CheckboxGroup, CheckboxButtonGroup, RadioButtonGroup, Div
from bokeh.io import curdoc
from bokeh.server.server import Server
from bokeh.embed import server_document

env = Environment(loader=FileSystemLoader('templates'))
class IndexHandler(RequestHandler):
    def get(self):
        template = env.get_template('embed.html')
        script = server_document('http://localhost:5006/main')
        self.write(template.render(script=script, template="Tornado"))

def modify_doc(doc):
    files = os.listdir(join(dirname(__file__), 'docs'))
    directions = []
    for file in range(len(files)):
        directions.append([files[file].split()[i] for i in range(len(files[file].split()))])
        directions[file][-1] = directions[file][-1].replace('.XLS', '')
        
    def update(attr, old, new):

        def sort(attr, old, new):
            did = False
            res = []
            temp = []
            for i in checkbox_button_group.active:
                for line in range(df_new.shape[0]):
                    #print(df_new[df_new.columns.values[4]][line])  
                    if button_labels[i] == df_new[df_new.columns.values[4]][line]:
                        temp.append(line)
                        did = True
                    if button_labels[i] == df_new[df_new.columns.values[5]][line]:
                        temp.append(line)
                        did = True

            if did == True:
                res = [item for item in df_new.index.values.tolist() if item not in temp]
            df_new_new = df_new.drop(res).reset_index(drop=True)
            source.data = {df_new_new.columns.values[column] : df_new_new[df_new_new.columns.values[column]] for column in range(df_new_new.shape[1])}

        df_new = df_initial
        for i in checkbox_group.active:
            df = pd.read_excel(join(dirname(__file__), 'docs', files[i]), skiprows=5, usecols=[0,1,3,4,5,6,9])
            df[df.columns.values[6]] = df[df.columns.values[6]].fillna('')
            for line in df[df.columns.values[6]].index:
                if df.loc[line,df.columns.values[6]] != '':
                    df.loc[line, df.columns.values[6]] = ' '.join(directions[i][1:]) 
            df_new = pd.merge(df_new, df,
                            how='outer',
                            on=df.columns.values.tolist())
            df_new = df_new.sort_values(by = df_new.columns.values[6], ascending=False)
            df_new = df_new.drop_duplicates(df_new.columns.values[1], keep='first')
            df_new = df_new.sort_values(by = df_new.columns.values[0])
        df_new = df_new.drop(df_new.columns.values[0], axis=1).reset_index(drop=True)
        
        button_labels = pd.concat([df_new[df_new.columns.values[4]], df_new[df_new.columns.values[5]]]).unique().tolist()
        del button_labels[button_labels.index('')]
        checkbox_button_group = CheckboxButtonGroup(labels=button_labels, width=1000)
        control_button = widgetbox(checkbox_button_group)
        l.children[0] = control_button
        checkbox_button_group.on_change('active', sort) 
        
        source.data = {df_new.columns.values[column] : df_new[df_new.columns.values[column]] for column in range(df_new.shape[1])}


    labels = [' '.join(directions[i]) for i in range(len(directions))]
    checkbox_group = CheckboxGroup(labels=labels)
    checkbox_group.on_change('active', update)

    df_initial = pd.read_excel(join(dirname(__file__), 'docs', files[0]), skiprows=5, usecols=[0,1,3,4,5,6,9], nrows=0) 
    source = ColumnDataSource(data = dict())
    columns = [TableColumn(field=df_initial.columns.values[column], title=df_initial.columns.values[column]) for column in range(1, df_initial.shape[1])]
    data_table = DataTable(source=source, columns=columns, width=1000, height = 2000)

    control = widgetbox(checkbox_group)
    table = widgetbox(data_table)
    l = layout(children=[widgetbox(CheckboxButtonGroup()), widgetbox(DataTable())])
    l.children[1] = table

    doc.add_root(row(control, l))

server = Server({'/main': modify_doc}, io_loop=IOLoop())
server.start()
if __name__ == '__main__':
    from bokeh.util.browser import view
    server.io_loop.add_callback(view, 'http://localhost:5006/')
    server.io_loop.start()