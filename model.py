from sqlalchemy import *
#Column, Integer, Text, Float, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    offensive_stats = relationship('Offensive_Stats', back_populates='team')
    defensive_stats = relationship('Defensive_Stats', back_populates='team')
    ws_winners = relationship('WS_Winners', back_populates='team')


class Offensive_Stats(Base):
    __tablename__ = 'offensive_stats'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    league = Column(Text)
    division = Column(Text)
    year = Column(Integer)
    wins = Column(Integer)
    runs_scored = Column(Integer)
    home_runs = Column(Integer)
    batting_avg = Column(Float)
    ops = Column(Float)
    avg_age = Column(Float)
    team = relationship('Team', back_populates='offensive_stats')


class Defensive_Stats(Base):
    __tablename__ = 'defensive_stats'
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id'))
    year = Column(Integer)
    losses = Column(Integer)
    runs_allowed = Column(Integer)
    earned_runs = Column(Integer)
    era = Column(Float)
    strikeouts = Column(Integer)
    field_percent = Column(Float)
    team = relationship('Team', back_populates='defensive_stats')


class WS_Winners(Base):
    __tablename__ = "ws_winners"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    year = Column(Integer)
    team_id = Column(Integer, ForeignKey('teams.id'))
    team = relationship('Team', back_populates="ws_winners")


#engine = create_engine('sqlite///:///mlb_stats.db', echo = True)
# Base.metadata.create_all(engine)
