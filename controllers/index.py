__author__ = 'Vince Maiuri'
import webapp2
import json
import urllib

from helpers import constants
from models.game import Game
from models.player import Player


def send_lobby(that, player_name=None):
    template = constants.JINJA_ENVIRONMENT.get_template('lobby.html')
    games = Game.get_all_games()
    template_values = {
        'games': games,
        'max_players': constants.MAX_PLAYERS,
    }

    if player_name:
        player = Player.get_player(player_name)
        template_values['player_name'] = player.name
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

        if game.add_player(player_name):
            ret_val['open'] = True
        else:
            ret_val['open'] = False
            if game.num_players < constants.MAX_PLAYERS:
                ret_val['reason'] = 'in-game'
            else:
                ret_val['reason'] = 'game-full'

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
