import dash
from dash_package import app2
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask
from dash_package.plots import *
from dash_package.dashboard import *


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']





app2.layout = html.Div(children=[
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=min(ws_years),
        max=max(ws_years),
        value=min(ws_years),
        marks={str(year): str(year) for year in ws_years}
    )
])

@app2.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])

def update_graph(year):
    traces = []
    runs_scored = osp.getOffensiveStatForEachTeamYear('runs_scored', year)[0]
    runs_allowed = dsp.getDefensiveStatForEachTeamYear('runs_allowed', year)
    # runs_list = [[x[0]]+[x[1]]+[y[1]] for x,y in zip(runs_scored, runs_allowed)]
    traces.append(go.Scatter(
        x=[i[1] for i in runs_scored],
        y=[i[1] for i in runs_allowed],
        text=[i[0] for i in runs_scored],
        mode='markers',
        opacity=0.7,
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'}
        },

    ))
    return {
    'data': traces}


# if __name__ == '__main__':
#     app2.run_server(debug=True)
