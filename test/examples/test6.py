from bokeh.models import Range1d

r = Range1d

# set properties individually:
r.start = 10
r.end = 20

# update properties together:
r.update(start=10, end=20)