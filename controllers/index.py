__author__ = 'Vince Maiuri'
import webapp2
import json
import urllib
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

        memcache.set_multi(game_dict, key_prefix='game-')
    else:
        games = []
        for key, value in games_dict.iteritems():
            games.append(value)

        games = sorted(games, key=lambda game: game.game_index)

    return games

def send_lobby(that, player_name=None):
    template = constants.JINJA_ENVIRONMENT.get_template('lobby.html')
    games = get_games()
    template_values = {
        'games': games,
        'max_players': constants.MAX_PLAYERS,
    }

    if player_name:
        template_values['player_name'] = player_name
        template_values['log_status'] = 'Log Out'

    that.response.write(template.render(template_values))


class Index(webapp2.RequestHandler):
    def get(self):
        player_name = self.request.get('player_name')
        if not player_name:
            return self.redirect('/login#login')

        send_lobby(self, player_name)


    def post(self):
        game_id = self.request.get('gameId')
        player_name = self.request.get('playerName')

        game = Game.get_game(game_id)

        ret_val = {}

        if game.add_player({'player_name': player_name}):
            ret_val['open'] = True
            memcache.set(game.game_index, game)
        else:
            ret_val['open'] = False

        self.response.write(json.dumps(ret_val))

class Login(webapp2.RequestHandler):
    def get(self):
        template = constants.JINJA_ENVIRONMENT.get_template('lobby.html')
        self.response.write(template.render({'player_name': '', 'log_status': 'Log In'}))

    def post(self):
        player_name = self.request.get("player_name")
        query_string = {'player_name': player_name}
        return self.redirect('/?{}'.format(urllib.urlencode(query_string)))

class Lobby(webapp2.RequestHandler):
    def get(self):
        send_lobby(self)
