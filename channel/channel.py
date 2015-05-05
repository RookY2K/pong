import json
from google.appengine.api import memcache
from google.appengine.api import channel
import webapp2

__author__ = 'Vince Maiuri'


def set_player(game_info):
    is_set = False
    game_pointer = game_info['game_pointer']
    player = game_info['player']
    client = memcache.Client()

    while not is_set:
        game_index = 'game{}'.format(game_pointer)

        game = memcache.get(game_index)

        if game is None:
            game = []
            memcache.set(game_index, game)

        if len(game) >= 2:
            while True:
                new_game_pointer = client.gets('game_pointer')
                if new_game_pointer > game_pointer:
                    game_pointer = new_game_pointer
                    break
                if client.cas('game_pointer', new_game_pointer):
                    game_pointer = new_game_pointer
                    break

            game_index = 'game{}'.format(game_pointer)

        while True:
            game = client.gets(game_index)
            if len(game) >= 2:
                break

            game.append(player)
            if client.cas(game_index, game):
                is_set = True
                break

    game_info['game_pointer'] = game_pointer
    return game_info


class Connect(webapp2.RequestHandler):
    def get(self):
        game_pointer = memcache.get('game_pointer')
        if game_pointer is None:
            game_pointer = 1
            memcache.set('game_pointer', game_pointer)

        user_name = self.request.get('userName')

        token = channel.create_channel(user_name)
        player = {
            'name': user_name,
            'token': token
        }
        self.response.write(json.dumps(player))

class Open(webapp2.RequestHandler):
    def post(self):
        player = self.request.get('player')
        game_pointer = memcache.get('game_pointer')

        game_info = {
            'player': player,
            'game_pointer': game_pointer
        }

        game_info = set_player(game_info)

        message = {
            'state': 'in-game',
            'game_info': game_info
        }

        channel.send_message(player['token'], json.dumps(message))