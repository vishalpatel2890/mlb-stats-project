from dash_package.scraping import *
import plotly as plt
import plotly.graph_objs as go
from flask_sqlalchemy import SQLAlchemy
import pdb

#returns appropriate graph objects
class DrawPlot:
    #init method gets all defensive and offensive stats
    def __init__(self):
        self.ds = DefensiveStats()
        self.os = OffensiveStats()

        self.offensive_keys = [('Wins', 'wins'), ('Average Age', 'avg_age'), ('OPS', 'ops'), ('Home Runs', 'home_runs'),
                        ('Batting Average', 'batting_avg'), ('Runs Scored', 'runs_scored')]
        self.defensive_keys = [('Losses', 'losses'), ('Runs Allowed', 'runs_allowed'), ('Earned Runs', 'earned_runs'),
                        ('ERA', 'era'), ('Strikeouts', 'strikeouts'), ('Fielding Perenctage', 'field_percent')]
        self.all_keys = [('Wins', 'wins'), ('Average Age', 'avg_age'), ('OPS', 'ops'), ('Home Runs', 'home_runs'),
                  ('Batting Average', 'batting_avg'), ('Runs Scored', 'runs_scored'), ('Losses', 'losses'),
                  ('Runs Allowed', 'runs_allowed'), ('Earned Runs', 'earned_runs'), ('ERA', 'era'),
                  ('Strikeouts', 'strikeouts'), ('Fielding Perenctage', 'field_percent')]
        self.off_keys = [x[1] for x in self.offensive_keys]
        self.def_keys = [x[1] for x in self.defensive_keys]

    #returns bar plot object for given year and stats for all mlb teams
    def createBarPlotForOffensiveStatYear(self, stat, year):
        year_stat_data, ws_winner_index = self.os.getOffensiveStatForEachTeamYear(stat, year)
        #list of colors matching length of # of teams
        # replace color matching index of ws winner
        colors = ['rgba(204,204,204,1)' for team in year_stat_data]
        colors[ws_winner_index] = 'rgba(222,45,38,0.8)'
        data = [go.Bar(
                x=[team[0] for team in year_stat_data],
                y=[team[1] for team in year_stat_data],
                marker=dict(
                    color=colors)
                )]
        return data

    def createBarPlotForDefensiveStatYear(self, stat, year):
        year_stat_data, ws_winner_index = self.ds.getDefensiveStatForEachTeamYear(stat, year)
        #list of colors matching length of # of teams
        # replace color matching index of ws winner
        colors = ['rgba(204,204,204,1)' for team in year_stat_data]
        colors[ws_winner_index] = 'rgba(222,45,38,0.8)'
        data = [go.Bar(
                x=[team[0] for team in year_stat_data],
                y=[team[1] for team in year_stat_data],
                marker=dict(
                    color=colors)
                )]
        return data
    #returns correct list of statistics depending if stat is offensive or defensive
    def key_find(self, stat, year):
        if stat in self.def_keys:
            return self.ds.getDefensiveStatForEachTeamYear(stat, year)[0]
        else:
            return self.os.getOffensiveStatForEachTeamYear(stat, year)[0]

    #returns scatter plot comparing any two stats for given year for all mlb teams
    def createScatterPlotForStatYear(self, year, stat1, stat2):
        #first drop down statistics query
        number_of_teams = self.key_find(stat1, year)
        #second drop down statistics query
        number_of_teams2 = self.key_find(stat2, year)
        #identify world series winner by year
        ws_winner = WS_Winners.query.filter(WS_Winners.year == year)[0].team.name
        index = [(i, el.index(ws_winner)) for i, el in enumerate(number_of_teams) if ws_winner in el][0][0]
        #list of colors matching length of # of teams
        # replace color matching index of ws winner
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
    #initialize CleanData class and list of team_name
    def __init__(self):
        self.cd = CleanData()
        self.team_names = self.cd.getTeamNames()

    #get single teams defensive stats
    def getTeamDefensiveStats(self, team_name):

        team_defensive_stats = Team.query.filter(Team.name == team_name)[0].defensive_stats
        return team_defensive_stats

    #needs to be completed - function to get single teams defensive stats for a range of years
    def getDefensiveStat(self, stat, team_name, year_start=None, year_end=None):
        team_defensive_stats = self.getTeamDefensiveStats(team_name)
        if year_start and year_end:
            stat_list = []
        else:
            stat_list = [(getattr(year, stat), year.year) for year in team_defensive_stats]
        return stat_list

    #return list of team name and respective defensive stat in a given year
    def getDefensiveStatForEachTeamYear(self, stat, year):
        year_stats = self.cd.getTeamsDefensiveStatsForYear(year)
        given_stat_year = [[team.team.name, getattr(team, stat)] for team in year_stats]
        ws_winner = WS_Winners.query.filter(WS_Winners.year == year)[0].team.name
        index = [(i, el.index(ws_winner)) for i, el in enumerate(given_stat_year) if ws_winner in el][0][0]
        return [given_stat_year,index]


class OffensiveStats:
    #initialize CleanData class and list of team_name
    def __init__(self):
        self.cd = CleanData()
        self.team_names = self.cd.getTeamNames()

    #get single teams offensive stats
    def getTeamOffensiveStats(self, team_name):
        team_offensive_stats = Team.query.filter(Team.name == team_name)[0].offensive_stats
        return team_offensive_stats

    #needs to be completed - function to get single teams offensive stats for a range of years
    def getOffensiveStatForTeam(self, stat, team_name, year_start=None, year_end=None):
        team_offensive_stats = self.getTeamOffensiveStats(team_name)
        if year_start and year_end:
            stat_list = []
        else:
            stat_list = [(getattr(year, stat), year.year) for year in team_offensive_stats]
        return stat_list

    #return list of team name and respective offensive stat in a given year
    #also return index of world series winner in the list
    def getOffensiveStatForEachTeamYear(self, stat, year):
        #all offesnive stats in a given year
        year_stats = self.cd.getTeamsOffensiveStatsForYear(year)
        #list of specific stats for each team
        given_stat_year = [[team.team.name, getattr(team, stat)] for team in year_stats]
        #team name of ws winner and index at which they are in the above list
        ws_winner = WS_Winners.query.filter(WS_Winners.year == year)[0].team.name
        index = [(i, el.index(ws_winner)) for i, el in enumerate(given_stat_year) if ws_winner in el][0][0]
        return [given_stat_year, index]

#inital queries of database
class CleanData:
    #return list of team names
    def getTeamNames(self):
        teams = Team.query.all()
        team_names = [team.name for team in teams]
        return team_names
    #get all offensive stats in a year
    def getTeamsOffensiveStatsForYear(self, year):
        offensive_stats_for_year = Offensive_Stats.query.filter(Offensive_Stats.year == year).all()
        return offensive_stats_for_year
    #get all defensive stats in a year
    def getTeamsDefensiveStatsForYear(self, year):
        defensive_stats_for_year = Defensive_Stats.query.filter(Defensive_Stats.year == year).all()
        return defensive_stats_for_year

    #return all years where there is valid WS series
    #some years there is no corressponding team object because of team name/franchise changes - needs to be fixed
    def getAllYearsWithValidWSWinner(self):
        ws_winners_with_team = WS_Winners.query.filter(WS_Winners.team_id).all()
        years = sorted([winner.year for winner in ws_winners_with_team])
        return years
