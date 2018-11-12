from scraping import *
import sqlalchemy

placeholder = Team(name='default')

sb = TeamStatsBuilder()
x = sb.run()


ws = WSStatsBuilder()
y = ws.run()

session.query(WS_Winners).filter(WS_Winners.name == 'Boston Redsox')[0].team = session.query(WS_Winners).filter(Team.name='Boston Red Sox')[0]
