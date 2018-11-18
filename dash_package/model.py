#wrapping dash around flask
from dash_package import db

#creating team table
#no relationship need defining due to use of Dash
class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

#creating offensive stats table
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

#creating defensive stats table
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

#creating table of world series winners
class WS_Winners(db.Model):
    __tablename__ = "ws_winners"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    year = db.Column(db.Integer)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship('Team', backref=db.backref('ws_winners', lazy=True))
