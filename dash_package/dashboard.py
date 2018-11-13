import dash
from dash_package import app
import dash_core_components as dcc
import dash_html_components as html
from dash_package.plots import *
import plotly.graph_objs as go

cd = CleanData()
dr = DrawPlot()
os = OffensiveStats()
years = cd.getAllYearsWithValidWSWinner()[-30:-1]

year_stat_data, ws_winner_index = os.getOffensiveStatForEachTeamYear('wins', 2018)
colors = ['rgba(204,204,204,1)' for team in year_stat_data]
colors[ws_winner_index] = 'rgba(222,45,38,0.8)'

app.layout = html.Div(children=[
    html.H1(children='Relationship Between Offensive Stats and World Series Winners'),

    dcc.Graph(id='offensive-stats'),
    dcc.Slider(
        id='year-slider',
        min=min(years),
        max=max(years),
        value=min(years),
        marks={str(year): str(year) for year in years}
    )
])


@app.callback(
    dash.dependencies.Output('offensive-stats', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')])
def update_graph(selected_year):
    data = dr.createBarPlotForOffensiveStatYear('wins', selected_year)


    #offensive_stats_for_year = session.query(Offensive_Stats).filter(Offensive_Stats.year == year).all()
    return {
        'data': data
    }
