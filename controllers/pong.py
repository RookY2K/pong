__author__ = 'Vince Maiuri'

import webapp2
import urllib

from helpers import constants
from models.player import Player
from models.game import Game

class Pong(webapp2.RequestHandler):
    def get(self):
        player_name = self.request.get('playerName')
        game_id = self.request.get('gameId')

        template_values = {
            'player_name': player_name,
            'game_id': game_id
        }

        template = constants.JINJA_ENVIRONMENT.get_template('pong.html')
        self.response.write(template.render(template_values))

class LeaveGame(webapp2.RequestHandler):
    def get(self):
        player_name = self.request.get('player_name')
        query_str = {'player_name': player_name}
        return self.redirect('/?{}'.format(urllib.urlencode(query_str)))

    def post(self):
        player_name = self.request.get('from')
        self.leave_game(player_name)

    def leave_game(self, player_name):
        player = Player.get_player(player_name)
        game_id = player.game_id

        game = Game.get_game(game_id)
        if game.remove_player(player_name):
            return self.redirect('/')
        else:
            return self.response.http_status_message(404)
