import os
import jinja2

__author__ = 'RookY2K'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '../views')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

MAX_PLAYERS = 2
MAX_GAMES = 8