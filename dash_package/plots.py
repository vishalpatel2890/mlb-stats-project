from dash_package.scraping import *
import plotly as plt
import plotly.graph_objs as go
from flask_sqlalchemy import SQLAlchemy
import pdb

class DrawPlot:
    def __init__(self):
        self.ds = DefensiveStats()
        self.os = OffensiveStats()

    def createBarPlotForOffensiveStatYear(self, stat, year):
        year_stat_data, ws_winner_index = self.os.getOffensiveStatForEachTeamYear(stat, year)
        colors = ['rgba(204,204,204,1)' for team in year_stat_data]
        colors[ws_winner_index] = 'rgba(222,45,38,0.8)'
        data = [go.Bar(
                x=[team[0] for team in year_stat_data],
                y=[team[1] for team in year_stat_data],
                marker=dict(
                    color=colors)
                )]
        return data

    offensive_keys = [('Wins', 'wins'), ('Average Age', 'avg_age'), ('OPS', 'ops'), ('Home Runs', 'home_runs'),
                    ('Batting Average', 'batting_avg'), ('Runs Scored', 'runs_scored')]
    defensive_keys = [('Losses', 'losses'), ('Runs Allowed', 'runs_allowed'), ('Earned Runs', 'earned_runs'),
                    ('ERA', 'era'), ('Strikeouts', 'strikeouts'), ('Fielding Perenctage', 'field_percent')]
    all_keys = [('Wins', 'wins'), ('Average Age', 'avg_age'), ('OPS', 'ops'), ('Home Runs', 'home_runs'),
              ('Batting Average', 'batting_avg'), ('Runs Scored', 'runs_scored'), ('Losses', 'losses'),
              ('Runs Allowed', 'runs_allowed'), ('Earned Runs', 'earned_runs'), ('ERA', 'era'),
              ('Strikeouts', 'strikeouts'), ('Fielding Perenctage', 'field_percent')]
    off_keys = [x[1] for x in offensive_keys]
    def_keys = [x[1] for x in defensive_keys]

    def key_find(self, stat, year):

        if stat in self.def_keys:
            return self.ds.getDefensiveStatForEachTeamYear(stat, year)
        else:
            return self.os.getOffensiveStatForEachTeamYear(stat, year)[0]

    def createScatterPlotForStatYear(self, year, stat1, stat2):
        number_of_teams = self.key_find(stat1, year)
        number_of_teams2 = self.key_find(stat2, year)
        ws_winner = WS_Winners.query.filter(WS_Winners.year == year)[0].team.name
        index = [(i, el.index(ws_winner)) for i, el in enumerate(number_of_teams) if ws_winner in el][0][0]

        colors = ['rgba(204,204,204,1)' for team in number_of_teams]
        colors[index] = 'rgba(222,45,38,0.8)'
        traces = []
        traces.append(go.Scatter(
                x=[i[1] for i in number_of_teams],
                y=[i[1] for i in number_of_teams2],
                text=[i[0] for i in number_of_teams],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'},
                    'color': colors},
                    ))
        return traces


class DefensiveStats:
    def __init__(self):
        self.cd = CleanData()
        self.team_names = self.cd.getTeamNames()

    def getTeamDefensiveStats(self, team_name):

        team_defensive_stats = Team.query.filter(Team.name == team_name)[0].defensive_stats
        return team_defensive_stats

    def getDefensiveStat(self, stat, team_name, year_start=None, year_end=None):
        team_defensive_stats = self.getTeamDefensiveStats(team_name)
        if year_start and year_end:
            stat_list = []
        else:
            stat_list = [(getattr(year, stat), year.year) for year in team_defensive_stats]
        return stat_list

    def getDefensiveStatForEachTeamYear(self, stat, year):
        year_stats = self.cd.getTeamsDefensiveStatsForYear(year)
        given_stat_year = [[team.team.name, getattr(team, stat)] for team in year_stats]
        print('from defensive stats')
        print(year_stats)
        print(stat)
        return given_stat_year


class OffensiveStats:
    def __init__(self):
        self.cd = CleanData()
        self.team_names = self.cd.getTeamNames()

    def getTeamOffensiveStats(self, team_name):
        team_offensive_stats = Team.query.filter(Team.name == team_name)[0].offensive_stats
        return team_offensive_stats

    def getOffensiveStatForTeam(self, stat, team_name, year_start=None, year_end=None):
        team_offensive_stats = self.getTeamOffensiveStats(team_name)
        if year_start and year_end:
            stat_list = []
        else:
            stat_list = [(getattr(year, stat), year.year) for year in team_offensive_stats]
        return stat_list

    def getOffensiveStatForEachTeamYear(self, stat, year):
        year_stats = self.cd.getTeamsOffensiveStatsForYear(year)
        given_stat_year = [[team.team.name, getattr(team, stat)] for team in year_stats]
        ws_winner = WS_Winners.query.filter(WS_Winners.year == year)[0].team.name
        index = [(i, el.index(ws_winner)) for i, el in enumerate(given_stat_year) if ws_winner in el][0][0]
        return [given_stat_year, index]


class CleanData:
    def getTeamNames(self):
        teams = Team.query.all()
        team_names = [team.name for team in teams]
        return team_names

    def getTeamsOffensiveStatsForYear(self, year):
        offensive_stats_for_year = Offensive_Stats.query.filter(Offensive_Stats.year == year).all()
        return offensive_stats_for_year

    def getTeamsDefensiveStatsForYear(self, year):
        defensive_stats_for_year = Defensive_Stats.query.filter(Defensive_Stats.year == year).all()
        return defensive_stats_for_year

    def getAllYearsWithValidWSWinner(self):
        ws_winners_with_team = WS_Winners.query.filter(WS_Winners.team_id).all()
        years = [winner.year for winner in ws_winners_with_team]
        return years

dsp = DefensiveStats()
osp = OffensiveStats()

def runs(year):
    runs_scored = osp.getOffensiveStatForEachTeamYear('runs_scored', year)[0]
    runs_allowed = dsp.getDefensiveStatForEachTeamYear('runs_allowed', year)[0]
    runs_list = [[x[0]]+[x[1]]+[y[1]] for x,y in zip(runs_scored, runs_allowed)]
    return runs_list
#test_year = runs(2017)

def ws_winners_years():
    ws_list = WS_Winners.query.filter(WS_Winners.team_id).all()
    return ws_list
ws_years = [x.year for x in ws_winners_years()][-40:-1]
