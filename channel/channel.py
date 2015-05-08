import json
from google.appengine.api import channel
import webapp2

from models.game import Game
from models.player import Player

__author__ = 'Vince Maiuri'


class Connect(webapp2.RequestHandler):
    def get(self):
        game_id = self.request.get('gameId')
        player_name = self.request.get('playerName')
        token = channel.create_channel(player_name)

        player_ret = {
            'player_name': player_name,
            'token': token,
            'game_id': game_id
        }

        player = Player.get_player(player_name)

        player.add_token(token)

        self.response.write(json.dumps(player_ret))


class Open(webapp2.RequestHandler):
    def post(self):
        player = self.request.get('player_info')
        player = json.loads(player)
        game_id = player['game_id']

        game = Game.get_game(game_id)

        player_num = game.incr_ready()

        if player_num == 1:
            side = 'left'
        else:
            side = 'right'

        message = {
            'state': 'in-game',
            'side': side,
            'player_num': player_num,
            'ready': game.ready
        }

        channel.send_message(player['token'], json.dumps(message))