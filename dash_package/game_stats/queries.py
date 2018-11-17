from dash_package.plots import *
from dash_package.game_stats.models import *

class CollectGameData:
    def getTeamsHomeGameAgainstMatchUp(self, team_code, team_code_2):
        team_alias = db.aliased(Team)
        team = Team.query.filter(Team.shortcode == team_code)[0]
        team2 = Team.query.filter(Team.shortcode == team_code_2)[0]
        home_games_matchup = db.session.query(Game).\
                    join(Game.h_team).\
                    join(team_alias, Game.v_team).\
                    filter(Game.h_team == team).\
                    filter(Game.v_team == team2).\
                    all()
        return home_games_matchup

    def getTeamsAwayGameAgainstMatchUp(self, team_code, team_code_2):
        team_alias = db.aliased(Team)
        team = Team.query.filter(Team.shortcode == team_code)[0]
        team2 = Team.query.filter(Team.shortcode == team_code_2)[0]
        away_games_matchup = db.session.query(Game).\
                    join(Game.h_team).\
                    join(team_alias, Game.v_team).\
                    filter(Game.h_team == team2).\
                    filter(Game.v_team == team).\
                    all()
        return away_games_matchup

    def getTeamsHomeGame(self, team_code):
        home_games = Game.query.join(Game.h_team, aliased = True).filter_by(shortcode = team_code).all()
        return home_games

    def getTeamsAwayGame(self, team_code):
        away_games = Game.query.join(Game.v_team, aliased = True).filter_by(shortcode = team_code).all()
        return away_games

    def allGames(self, team_code):
        all_games = self.getTeamsAwayGame(team_code) + self.getTeamsHomeGame(team_code)
        return all_games

class Matchups:
    pass
