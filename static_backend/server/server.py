__author__ = 'Vince Maiuri'

import webapp2
import threading
import time
from google.appengine.api import background_thread, memcache
from static_backend.game_objects import player
from static_backend.backend_channel import channel


class Start(webapp2.RequestHandler):
    def get(self):
        background_thread.BackgroundThread(target=server_start).start()
        self.response.http_status_message(200)


def server_start():
    games = {
        'number': 1,
        'games': {}
    }

    timer_interval = .0035
    physics_interval = .0145
    client_update_interval = .0445
    get_input_interval = .0125

    while True:
        players = []
        game_number = games['number']
        game_index = None

        while len(players) < 2:
            cur_game_pointer = memcache.get('game_pointer')
            if cur_game_pointer < game_number:
                continue

            game_index = 'game{}'.format(game_number)
            players_get = memcache.get(game_index)
            if players_get:
                players = players_get

        game_info = {
            'intervals': {
                'timer': timer_interval,
                'physics': physics_interval,
                'client': client_update_interval,
                'get_input': get_input_interval
            },
            'players': players,
            'game_index': game_index
        }

        if game_index:
            background_thread.BackgroundThread(target=start_game, name=game_index, kwargs=game_info)


def start_game(game_info):
    players = game_info['players']
    player1_name = players[0]['name']

    player2_name = players[1]['name']
    player1_token = players[0]['token']
    player2_token = players[1]['token']
    player1 = player.Player(player1_name, 'left', game_info['game_index'], player1_token)
    player2 = player.Player(player2_name, 'right', game_info['game_index'], player2_token)

    msg1 = {
        'state': 'opponent-notification',
        'message': 'Opponent = {}'.format(player2.user_name)
    }
    msg2 = {
        'state': 'opponent-notification',
        'message': 'Opponent = {}'.format(player1.user_name)
    }

    channel.send_message_to_client(msg1, player1.token)
    channel.send_message_to_client(msg2, player2.token)



def update_loop(update_function, interval):
    start_time = time.time() * 1000
    update_function()
    timer = max(0, interval - ((time.time() * 1000 - start_time)))
    threading._Timer(timer, update_loop, [update_function, interval])


