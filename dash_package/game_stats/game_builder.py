from dash_package.game_stats.collect_data import *
from dash_package.game_stats.models import *

class GameBuilder:
    def buildGame(self):
        ggd = GetGameData()
        games = []
        for index, games_data in ggd.getGameDataForYear().iterrows():
            try:
                new_game = Game(
                            date = games_data['date'],
                            v_team = db.session.query(Team).filter(Team.shortcode == games_data['Visiting Team'])[0],
                            v_team_league = games_data['Visiting Team League'],
                            h_team = db.session.query(Team).filter(Team.shortcode == games_data['Home Team'])[0],
                            h_team_league = games_data['Home Team League'],
                            v_score = games_data['Visiting Score'],
                            h_score = games_data['Home Score'],
                            park = games_data['Park ID'],
                            v_line_score = games_data['Visiting Line Score'],
                            h_line_score = games_data['Home Line Score'],
                            v_at_bats = games_data['Visiting At Bats'],
                            v_hits = games_data['Visiting Hits'],
                            v_home_runs = games_data['Visiting Home Runs'],
                            h_at_bats = games_data['Home At Bats'],
                            h_hits  = games_data['Home Hits'],
                            h_home_runs = games_data['Home Home Runs'],
                            w_pitcher_id = games_data['Winning Pitcher ID'],
                            w_pitcher_name = games_data['Winning Pitcher Name'],
                            l_pitcher_id = games_data['Losing Pitcher ID'],
                            l_pitcher_name = games_data['Losing Pitcher Name'],
                            acquisition_info = games_data['Acquisition Information']
                             )
            except:
                pass
            games.append(new_game)
        return games
