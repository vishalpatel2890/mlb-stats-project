from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dash

#stylesheets for dash app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#intialize Flask server and config variables
server = Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///baseball.db'
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
server.config["SQLALCHEMY_ECHO"] = False

#connect flask and sqlalchemy
db = SQLAlchemy(server)

#initialize dash apps
app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/', external_stylesheets=external_stylesheets)
app2 = dash.Dash(__name__, server=server, url_base_pathname='/dash/', external_stylesheets=external_stylesheets)

#import dash apps for export 
from dash_package.dashboard import *
from dash_package.plots import *
from dash_package.model import *
from dash_package.app2 import *
