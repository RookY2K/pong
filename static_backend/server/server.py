__author__ = 'Vince Maiuri'

import webapp2
from threading import Thread, Event
import time
from google.appengine.api import background_thread
from backend_models.game import Game
from backend_models.player import Player
from game_helpers import constants
from game_objects import player
from update_engines import physics, update_clients, update_timer
from backend_channel import channel
import inputs




class Start(webapp2.RequestHandler):
    def post(self):
        game_id = self.request.get('gameId')

        background_thread.BackgroundThread(target=game_start, args=[game_id, ]).start()
        self.response.http_status_message(200)


def game_start(game_id):
    timer_interval = .0035
    physics_interval = .0145
    client_update_interval = .0445

    game = Game.get_game(game_id)
    players = {}
    player_list = []
    for i in range(len(game.players)):
        player_name = game.players[i]
        player_model = Player.get_player(player_name)
        if i == 0:
            side = 'left'
        elif i == 1:
            side = 'right'

        players[side] = player.Player(player_name, side, game_id, player_model.token)
        player_list.append(players[side])
        inputs.global_game_players[player_name] = players[side]

    start_game_info = {
        'state': 'start-game',
        'server_time': (time.time() * 1000)
    }

    # game_info = {
    #     'left': players['left'],
    #     'right': players['right']
    # }

    # game_stop_flag = Event()
    # game_loop = UpdateThread(start_game, 10000, game_stop_flag, [game_info, ])
    # game_loop.start()

    timer_obj = update_timer.UpdateTimer()
    timer_stop_flag = Event()
    timer_loop = UpdateThread(timer_obj.update_timer, timer_interval, timer_stop_flag)
    timer_loop.start()

    physics_obj = physics.PhysicsEngine(player_list, None)
    physics_stop_flag = Event()
    physics_loop = UpdateThread(physics_obj.update, physics_interval, physics_stop_flag)
    physics_loop.start()

    client_update_obj = update_clients.UpdateClients(player_list, timer_obj)
    client_update_stop_flag = Event()
    client_update_loop = UpdateThread(client_update_obj.update, client_update_interval, client_update_stop_flag)
    client_update_loop.start()

    channel.send_message_to_client(start_game_info, players['left'].token)
    channel.send_message_to_client(start_game_info, players['right'].token)

    while True:
        game = Game.get_game(game_id)
        if game.ready < constants.MAX_PLAYERS:
            # game_stop_flag.set()
            timer_stop_flag.set()
            physics_stop_flag.set()
            client_update_stop_flag.set()
            for player_obj in player_list:
                inputs.remove_player_inputs(player_obj.player_name)
            break


def start_game(args):
    game_info = args[0]
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

    channel.send_message_to_client(msg1, left_player.player_name)
    channel.send_message_to_client(msg2, right_player.player_name)


class UpdateThread(Thread):
    def __init__(self, func, interval, stop_event, args=None):
        Thread.__init__(self)
        self.func = func
        self.interval = interval
        self.args = args
        self.stopped = stop_event

    def run(self):
        timer = 0.0
        while not self.stopped.wait(timer / 1000):
            start_time = time.time() * 1000
            if self.args:
                self.func(self.args)
            else:
                self.func()
            timer = max(0, self.interval - ((time.time() * 1000) - start_time))