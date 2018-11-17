import pandas as pd

class GetGameData:
    def getGameDataForYear(self):
        years_games = pd.read_csv('./dash_package/game_stats/data/GL2017.TXT', sep=",", header=None)
        years_games.rename(columns={0:'date',
                                    3: 'Visiting Team',
                                    4: 'Visiting Team League',
                                    6: 'Home Team',
                                    7: 'Home Team League',
                                    9: 'Visiting Score',
                                    10: 'Home Score',
                                    16: 'Park ID',
                                    19: 'Visiting Line Score',
                                    20: 'Home Line Score',
                                    21: 'Visiting At Bats',
                                    22: 'Visiting Hits',
                                    25: 'Visiting Home Runs',
                                    49: 'Home At Bats',
                                    50: 'Home Hits',
                                    51: 'Home Home Runs',
                                    93: 'Winning Pitcher ID',
                                    94: 'Winning Pitcher Name',
                                    95: 'Losing Pitcher ID',
                                    96: 'Losing Pitcher Name',
                                    160: 'Acquisition Information'
                                    }, inplace=True)
        return years_games
