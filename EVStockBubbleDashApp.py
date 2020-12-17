import pandas as pd
from datetime import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

volu = pd.read_pickle('EVStock2020Formatted.pickle')

scat = px.scatter(volu, x="Price", y="Percent", animation_frame="Day", animation_group="Sym",
           size="Volume", color="Sym", hover_name="Sym",
           log_x=True, log_y=False, size_max=350, range_x=[0.1,210], range_y=[-40,40],
                  text='Sym',
                  labels={
                     "Percent": "Percent Change",
                     "Price": "$ Price"
                 },
                  title='')

scat.update_layout(
    title={
        'y':0,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})

''' Code to add changing date in title '''
''' Issues include choppy play while viewing animated chart due to redraw '''
##dates = list(set(volu['Date']))
##dates = [x.strftime('%m/%d/%Y') for x in sorted(dates)]
##
##for button in scat.layout.updatemenus[0].buttons:
##    button['args'][1]['frame']['redraw'] = True
##
##for k in range(len(scat.frames)):
##    scat.frames[k]['layout'].update(title_text='Date: {}'.format(dates[k]))

scat.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000
scat.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 1000

animations = {
    'Scatter': scat
}

app = dash.Dash(__name__)

app.layout = html.Div([
    html.P("Select an animation:"),
    dcc.RadioItems(
        id='selection',
        options=[{'label': x, 'value': x} for x in animations],
        value='Scatter'
    ),
    dcc.Graph(id="graph",
              figure={'layout':{'height':900,}
                  }),
])

@app.callback(
    Output("graph", "figure"), 
    [Input("selection", "value")])
def display_animated_graph(s):
    return animations[s]

app.run_server(debug=True)
