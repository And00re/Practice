from bokeh.models.widgets import TextInput
from bokeh.plotting import curdoc

def my_text_input_handler(attr, old, new):
    print("Previous label: " + old)
    print("Updated label: " + new)

text_input = TextInput(value="default", title="Label:")
text_input.on_change("value", my_text_input_handler)

curdoc().add_root(text_input)

#bokeh serve --show test4.py