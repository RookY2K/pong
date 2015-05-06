__author__ = 'Vince Maiuri'
import webapp2
from google.appengine.api import memcache

from helpers import constants
from models.game import Game

def get_games():
    game_range = [str(x) for x in range(1, constants.MAX_GAMES+1)]
    games_dict = memcache.get_multi(game_range, key_prefix='game-')
    if not games_dict:
        games = Game.get_all_games()
        game_dict = {}
        for i in range(len(games)):
            game_dict[str(game_range[i])] = games[i]

        memcache.set_multi(game_dict,key_prefix='game-')
    else:
        games = []
        for key, value in games_dict.iteritems():
            games.append(value)

        games = sorted(games, key=lambda game: game.game_index)

    return games


class Index(webapp2.RequestHandler):
    def get(self):
        template = constants.JINJA_ENVIRONMENT.get_template('lobby.html')
        games = get_games()
        template_values = {'games': games, 'max_players': constants.MAX_PLAYERS}
        self.response.write(template.render(template_values))
