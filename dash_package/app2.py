import dash
from dash_package import app2
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask
from dash_package.plots import *
from dash_package.dashboard import *


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

cd = CleanData()
dr = DrawPlot()
os = OffensiveStats()

number_of_teams, ws_winner_index = os.getOffensiveStatForEachTeamYear('runs_scored', 2018)
colors = ['rgba(204,204,204,1)' for team in number_of_teams]
colors[ws_winner_index] = 'rgba(222,45,38,0.8)'

app2.layout = html.Div(children=[
    html.H1(children='Comparing Two Stats and World Series Winners'),
    dcc.Dropdown(
                id='offensive-stat-selector',
                #get offesive keys for dropdown selector
                options=[{'label': key[0], 'value': key[1]} for key in dr.all_keys],
                value='wins'),
    dcc.Dropdown(
                id='defensive-stat-selector',
                #get offesive keys for dropdown selector
                options=[{'label': key[0], 'value': key[1]} for key in dr.all_keys],
                value='losses'),
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
    [dash.dependencies.Input('year-slider', 'value'),
    dash.dependencies.Input('offensive-stat-selector', 'value'),
    dash.dependencies.Input('defensive-stat-selector', 'value')])

def update_graph(year, stat1, stat2):
    traces = dr.createScatterPlotForStatYear(year, stat1, stat2)

    return{'data': traces,
    'layout': go.Layout(
    xaxis={'type': 'log', 'title': stat1},
    yaxis={'title': stat2},
    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
    legend={'x': 0, 'y': 1},
    hovermode='closest')}



# if __name__ == '__main__':
#     app2.run_server(debug=True)
