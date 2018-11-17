from dash_package.scraping import *
import sqlalchemy

placeholder = Team(name='default')

# # Create steamstatsbuilder class and store list of teams and their stats in variable x | session.commit()
# # in terminal or jupyer session.add_all(x) or for team in x: db.session.add(team)
# sb = TeamStatsBuilder()
# x = sb.run()
#
# # Create WS Stats Builder class and store list of WS winners in variable y | session.commit()
# # in terminal or jupyter session.add_all(y) or for winner in y: db.session.add(y)
# ws = WSStatsBuilder()
# y = ws.run()

# # To clean 'Boston redsox' error
# session.query(WS_Winners).filter(WS_Winners.name == 'Boston Redsox')[0].team = session.query(WS_Winners).filter(Team.name='Boston Red Sox')[0]
