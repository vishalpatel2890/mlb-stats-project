import pandas as pd
from dash_package import *



def changeTeamShortcode():
    teams = Team.query.all()
    df_shortcodes = pd.read_csv('./dash_package/game_stats/data/CurrentNames.csv', header = None)
    df_shortcodes['full name'] = df_shortcodes[4] + " " + df_shortcodes[5]
    updated_teams = []
    for team in teams:
        try:
            x = df_shortcodes[df_shortcodes['full name'] == team.name].iloc[0][0]
            team.shortcode = x
            updated_teams.append(team)
        except:
            print("Not Found",team.name)
    return updated_teams
