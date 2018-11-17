from flask import Blueprint
from dash_package.game_stats.seed import *
from dash_package.game_stats.queries import *
game_stats = Blueprint("game_stats", __name__)
