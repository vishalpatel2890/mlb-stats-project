import sqlalchemy Column, Integer, Text, Float
from sqlalcehmy.ext.declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Team(Base):
    __tablename__='teams'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    offensive_stats = relationship('Offensive_Stats', back_populates='team_id')
    defensive_stats = relationship('Defensive_Stats', back_populates='team_id')
    ws_winners = relationship('WS_Winners', back_populates='team_id')


class Offensive_Stats(Base):
    __tablename__='offensive_stats'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    league = Column(Text)
    division = Column(Text)
    year = Column(Integer)
    wins = Column(Integer)
    runs_scored = Column(Integer)
    home_runs = Column(Integer)
    batting_average = Column(Float)
    ops = Column(Float)
    avg_age = Column(Float)
    team = relationship('Team', back_populates='offensive_stats')


class Defensive_Stats(Base):
    __tablename__='defensive_stats'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    year = Column(Integer)
    losses = Column(Integer)
    runs_allowed = Column(Integer)
    earned_runs = Column(Integer)
    era = Column(Float)
    strikeouts =  Column(Integer)
    field_percent = Column(Float)
    defensive_stats = relationship('Team', back_populates='defensive_stats')

class WS_Winners(Base):
    __tablename__="ws_winners"
    id = Column(Integer)
    year = Column(Integer)
    team_id = Column(Integer, ForeignKey('teams.id'))
    ws_winners = relationship('Team', back_populates="ws_winners")









engine = creat_engine('sqlite///:///dbname', echo = True)
Base.metadata.creat_all(engine)
