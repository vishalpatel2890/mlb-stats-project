from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = Flask(__name__)
server.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///baseball.db'
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
server.config["SQLALCHEMY_ECHO"] = False

db = SQLAlchemy(server)

app = dash.Dash(__name__, server=server, url_base_pathname='/dashboard/', external_stylesheets=external_stylesheets)

from dash_package.dashboard import *
from dash_package.plots import *
from dash_package.model import *
