
import bokeh
import xlrd
import pandas as pd
import numpy
'''
book = xlrd.open_workbook('09.03.02 ИСиТ О Б.XLS')
sheet = book.sheet_by_index(0)
for row in range(5, sheet.nrows):
    print(sheet.row_values(row))
'''
df = pd.read_excel('09.03.02 ИСиТ О Б.XLS', skiprows=5, index_col=0)
print(df)