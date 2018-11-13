# from sqlalchemy import *
# #Column, Integer, Text, db.Float, db.ForeignKey, create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship, sessionmaker
#
# Base = declarative_base()

from dash_package import db


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    # remove for Flask SQL Alchemy
# offensive_stats = db.relationship('Offensive_Stats',  backref=db.backref('team', lazy=True))
# defensive_stats = db.relationship('Defensive_Stats',  backref=db.backref('team', lazy=True))
# ws_winners = db.relationship('WS_Winners', backref=db.backref('team', lazy=True))


class Offensive_Stats(db.Model):
    __tablename__ = 'offensive_stats'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    league = db.Column(db.Text)
    division = db.Column(db.Text)
    year = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    runs_scored = db.Column(db.Integer)
    home_runs = db.Column(db.Integer)
    batting_avg = db.Column(db.Float)
    ops = db.Column(db.Float)
    avg_age = db.Column(db.Float)
    team = db.relationship('Team', backref=db.backref('offensive_stats', lazy=True))


class Defensive_Stats(db.Model):
    __tablename__ = 'defensive_stats'
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    year = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    runs_allowed = db.Column(db.Integer)
    earned_runs = db.Column(db.Integer)
    era = db.Column(db.Float)
    strikeouts = db.Column(db.Integer)
    field_percent = db.Column(db.Float)
    team = db.relationship('Team', backref=db.backref('defensive_stats', lazy=True))


class WS_Winners(db.Model):
    __tablename__ = "ws_winners"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    year = db.Column(db.Integer)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship('Team', backref=db.backref('ws_winners', lazy=True))


#engine = create_engine('sqlite///:///mlb_stats.db', echo = True)
# Base.metadata.create_all(engine)
