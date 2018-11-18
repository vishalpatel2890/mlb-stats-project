import dash
from dash_package import app2
import dash_core_components as dcc
import dash_html_components as html
from flask import Flask
from dash_package.plots import *
from dash_package.dashboard import *


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#initalize CleanData, DrawPlot, Offensive Stats, class
cd = CleanData()
dr = DrawPlot()
os = OffensiveStats()

def ws_winners_years():
    ws_list = WS_Winners.query.filter(WS_Winners.team_id).all()
    return ws_list
#specify number of years that slider will compare in graph
ws_years = [x.year for x in ws_winners_years()][-40:-1]

#add layout to dash
app2.layout = html.Div(children=[
    html.H1(children='Comparing Two Stats and World Series Winners'),
    #dropdown selector #1
    dcc.Dropdown(
                id='offensive-stat-selector',
                #get all keys for dropdown selector
                options=[{'label': key[0], 'value': key[1]} for key in dr.all_keys],
                value='wins'),
    #dropdown selector #2
    dcc.Dropdown(
                id='defensive-stat-selector',
                #get all keys for dropdown selector
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

# create callbacks to dropdowns and year slider
@app2.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('year-slider', 'value'),
    dash.dependencies.Input('offensive-stat-selector', 'value'),
    dash.dependencies.Input('defensive-stat-selector', 'value')])

def update_graph(year, stat1, stat2):
    #returns offensive plot
    traces = dr.createScatterPlotForStatYear(year, stat1, stat2)

    return{'data': traces,
    'layout': go.Layout(
    #set x axis title equal to stat being displayed
    xaxis={'type': 'log', 'title': stat1},
    #set y axis title equal to stat being displayed
    yaxis={'title': stat2},
    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
    legend={'x': 0, 'y': 1},
    hovermode='closest')}
