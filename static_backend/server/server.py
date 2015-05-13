__author__ = 'Vince Maiuri'

import webapp2
from threading import Thread, Event
import time
from google.appengine.api import background_thread
from models.game import Game
from models.player import Player
from game_helpers import constants
from game_objects import player
from backend_channel import channel

game_inputs = {}


class Start(webapp2.RequestHandler):
    def post(self):
        game_id = self.request.get('gameId')

        background_thread.BackgroundThread(target=game_start, args=[game_id, ]).start()
        self.response.http_status_message(200)


class Input(webapp2.RequestHandler):
    def post(self):
        player_input = self.request.get('input')
        player_name = self.request.get('playerName')

        game_inputs[player_name] = player_input


def game_start(game_id):
    timer_interval = .0035
    physics_interval = .0145
    client_update_interval = .0445
    get_input_interval = .0125

    game = Game.get_game(game_id)
    players = {}
    for i in range(len(game.players)):
        player_name = game.players[i]
        player_model = Player.get_player(player_name)
        if i == 0:
            side = 'left'
        elif i == 1:
            side = 'right'

        players[side] = player.Player(player_name, side, game_id, player_model.token)

    start_game_info = {
        'state': 'start-game',
        'server_time': (time.time() * 1000)
    }

    game_info = {
        'left': players['left'],
        'right': players['right']
    }

    game_stop_flag = Event()
    game_loop = UpdateThread(start_game, 10000, game_stop_flag, [game_info, ])
    game_loop.start()

    channel.send_message_to_client(start_game_info, players['left'].token)
    channel.send_message_to_client(start_game_info, players['right'].token)

    while True:
        game = Game.get_game(game_id)
        if game.ready < constants.MAX_PLAYERS:
            game_stop_flag.set()
            break


def start_game(game_info):
    left_player = game_info['left']
    right_player = game_info['right']

    msg1 = {
        'state': 'opponent-notification',
        'message': 'Opponent = {}'.format(right_player.player_name)
    }
    msg2 = {
        'state': 'opponent-notification',
        'message': 'Opponent = {}'.format(left_player.player_name)
    }

    channel.send_message_to_client(msg1, left_player.token)
    channel.send_message_to_client(msg2, right_player.token)


class UpdateThread(Thread):
    def __init__(self, func, interval, stop_event, args):
        Thread.__init__(self)
        self.func = func
        self.interval = interval
        self.args = args
        self.stopped = stop_event

    def run(self):
        timer = 0.0
        while not self.stopped.wait(timer / 1000):
            start_time = time.time() * 1000
            self.func(self.args[0])
            timer = max(0, self.interval - ((time.time() * 1000) - start_time))