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
offensive_keys = [('Wins', 'wins'), ('Average Age', 'avg_age'), ('OPS', 'ops'), ('Home Runs', 'home_runs'),
                ('Batting Average', 'batting_avg'), ('Runs Scored', 'runs_scored')]
year_stat_data, ws_winner_index = os.getOffensiveStatForEachTeamYear('wins', 2018)
colors = ['rgba(204,204,204,1)' for team in year_stat_data]
colors[ws_winner_index] = 'rgba(222,45,38,0.8)'

app.layout = html.Div([
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(id='Tab 1', label='Offensive Stats', children=[
            html.H1(children='Relationship Between Offensive Stats and World Series Winners'),
            dcc.Dropdown(
                        id='stat-selector',
                        #get offesive keys for dropdown selector
                        options=[{'label': key[0], 'value': key[1]} for key in offensive_keys],
                        value='wins'
                    ),
            dcc.Graph(id='offensive-stats'),
            dcc.Slider(
                id='year-slider',
                min=min(years),
                max=max(years),
                value=min(years),
                marks={str(year): str(year) for year in years}
            )
            ]),
        dcc.Tab(id='Tab 2', label='Defensive Stats', children=[
            html.H1(children='Relationship Between Offensive Stats and World Series Winners'),
            
            ])
        ])
])


@app.callback(
    dash.dependencies.Output('offensive-stats', 'figure'),
    [dash.dependencies.Input('year-slider', 'value'),
    dash.dependencies.Input('stat-selector', 'value')]
    )

def update_graph(selected_year, selected_stat):
    data = dr.createBarPlotForOffensiveStatYear(selected_stat, selected_year)


    return {
        'data': data
    }
