import json
from google.appengine.api import memcache
from google.appengine.api import channel
import webapp2

from models.game import Game

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

        game = memcache.get(game_id)
        if not game:
            game = Game.get_game(game_id)

        game.add_player_token(player_name, token)
        memcache.set(game_id, game)

        self.response.write(json.dumps(player_ret))


class Open(webapp2.RequestHandler):
    def post(self):
        player = self.request.get('player_info')
        player = json.loads(player)
        game_id = player['game_id']

        game = memcache.get(game_id)

        if not game:
            game = Game.get_game(game_id)

        player_num = game.incr_ready()
        memcache.set(game_id, game)

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