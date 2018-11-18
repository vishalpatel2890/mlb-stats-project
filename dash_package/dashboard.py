import dash
from dash_package import app
import dash_core_components as dcc
import dash_html_components as html
from dash_package.plots import *
import plotly.graph_objs as go

#initalize CleanData, DrawPlot, Offensive Stats, class
cd = CleanData()
dr = DrawPlot()
os = OffensiveStats()
years = cd.getAllYearsWithValidWSWinner()[-30:-1]
print(years)
#list of offensive keys


year_stat_data, ws_winner_index = os.getOffensiveStatForEachTeamYear('wins', 2018)
colors = ['rgba(204,204,204,1)' for team in year_stat_data]
colors[ws_winner_index] = 'rgba(222,45,38,0.8)'

#add layout to dash
app.layout = html.Div([
    # tabs
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(id='Tab 1', label='Offensive Stats', children=[
            html.H1(children='Relationship Between Offensive Stats and World Series Winners'),
            dcc.Dropdown(
                        id='stat-selector',
                        #get offesive keys for dropdown selector
                        options=[{'label': key[0], 'value': key[1]} for key in dr.offensive_keys],
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
            html.H1(children='Relationship Between Defensive Stats and World Series Winners'),
            dcc.Dropdown(
                        id='defensive-stat-selector',
                        #get offesive keys for dropdown selector
                        options=[{'label': key[0], 'value': key[1]} for key in dr.defensive_keys],
                        value='losses'
                    ),
            dcc.Graph(id='defensive-stats'),
            dcc.Slider(
                id='defensive-year-slider',
                min=min(years),
                max=max(years),
                value=min(years),
                marks={str(year): str(year) for year in years}
            )
            ])
        ])
])

# create callbacks to dropdowns and year slider
@app.callback(
    dash.dependencies.Output('offensive-stats', 'figure'),
    [dash.dependencies.Input('year-slider', 'value'),
    dash.dependencies.Input('stat-selector', 'value')]
    )

#function runs when callback is triggered with new input values
def update_offensive_graph(selected_year, selected_stat):
    #returns offensive plot
    data = dr.createBarPlotForOffensiveStatYear(selected_stat, selected_year)


    return {
        'data': data
    }
#callback for updating defensive stats plot
@app.callback(
    dash.dependencies.Output('defensive-stats', 'figure'),
    [dash.dependencies.Input('defensive-year-slider', 'value'),
    dash.dependencies.Input('defensive-stat-selector', 'value')]
    )

def update_offensive_graph(selected_year, selected_stat):
    #returns offensive plot
    data = dr.createBarPlotForDefensiveStatYear(selected_stat, selected_year)


    return {
        'data': data
    }
