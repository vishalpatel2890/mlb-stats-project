from scraping import *


class DefensiveStats:
    def __init__(self):
        self.cd = CleanData()
        self.team_names = self.cd.getTeamNames()

    def getTeamDefensiveStats(self, team_name):
        team_defensive_stats = session.query(Team).filter(Team.name == team_name)[0].defensive_stats
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
        team_offensive_stats = session.query(Team).filter(Team.name == team_name)[0].offensive_stats
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
        return given_stat_year


class CleanData:
    def getTeamNames(self):
        teams = session.query(Team).all()
        team_names = [team.name for team in teams]
        return team_names

    def getTeamsOffensiveStatsForYear(self, year):
        offensive_stats_for_year = session.query(Offensive_Stats).filter(Offensive_Stats.year == year).all()
        return offensive_stats_for_year
