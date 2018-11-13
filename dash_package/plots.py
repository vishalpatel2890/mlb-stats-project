from dash_package.scraping import *
import plotly as plt
import plotly.graph_objs as go
from flask_sqlalchemy import SQLAlchemy


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


class DefensiveStats:
    def __init__(self):
        self.cd = CleanData()
        self.team_names = self.cd.getTeamNames()

    def getTeamDefensiveStats(self, team_name):
        team_defensive_stats = Team.query.filter_by(Team.name == team_name)[0].defensive_stats
        return team_defensive_stats

    def getDefensiveStat(self, stat, team_name, year_start=None, year_end=None):
        team_defensive_stats = self.getTeamDefensiveStats(team_name)
        if year_start and year_end:
            stat_list = []
        else:
            stat_list = [(getattr(year, stat), year.year) for year in team_defensive_stats]
        return stat_list


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

    def getAllYearsWithValidWSWinner(self):
        ws_winners_with_team = WS_Winners.query.filter(WS_Winners.team_id).all()
        years = [winner.year for winner in ws_winners_with_team]
        return years
