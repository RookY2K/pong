__author__ = 'Vince Maiuri'

import json
import webapp2
import urllib
from google.appengine.api import channel
from backend_models.player import Player
from backend_models.game import Game

global_start_ball = {}


def send_message_to_client(msg, token):
    print 'Sending message to {}: {}'.format(token, msg)
    channel.send_message(token, json.dumps(msg))


class StartBall(webapp2.RequestHandler):
    def post(self):
        game_id = self.request.get('gameId')
        global_start_ball[game_id] = True


class Connect(webapp2.RequestHandler):
    def get(self):
        game_id = self.request.get('gameId')
        player_name = self.request.get('playerName')
        token = channel.create_channel(player_name)
        global_start_ball[game_id] = False

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
        player_name = player['player_name']

        game_player = Player.get_player(player_name)

        game = Game.get_game(game_id)

        player_num = game.incr_ready()

        if player_num == 1:
            side = 'left'
        else:
            side = 'right'

        game_player.add_side(side)

        message = {
            'state': 'in-game',
            'side': side,
            'player_num': player_num,
            'ready': game.ready
        }

        channel.send_message(player['token'], json.dumps(message))


class LeaveGame(webapp2.RequestHandler):
    def get(self):
        player_name = self.request.get('player_name')
        query_str = {'player_name': player_name}
        self.leave_game(player_name)
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