from model import *
from sqlalchemy import create_engine

engine = create_engine('sqlite:///mlb_stats.db')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Red_Sox = Team(name='Boston Red Sox')
# Red_Sox_Offense = Offensive_Stats(team=Red_Sox, league='American', division='East', year=2018, wins=110, runs_scored=876, home_runs=208, batting_avg=.268, ops=.792, avg_age=27.7)
# #Red_Sox_Offense.team
# Red_Sox_Defense = Defensive_Stats(team=Red_Sox, year=2018, losses=54, runs_allowed=647, earned_runs=608, era=3.75, strikeouts=1558, field_percent=.987)
# WS_Winner_2018 = WS_Winners(year=2018, team=Red_Sox)


session.add(Red_Sox)
session.commit()
