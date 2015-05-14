__author__ = 'Vince Maiuri'
import time
from game_helpers import math


class PhysicsEngine:
    def __init__(self, players, ball):
        self.count = 0
        self.start_delta = .0001
        self.end_delta = time.time() * 1000
        self.players = players
        self.ball = ball

    def update(self):
        self.start_delta = ((time.time() * 1000) - self.end_delta) / 1000.0
        self.end_delta = time.time() * 1000
        if self.players is not None:
            self.physics_engine()

    def physics_engine(self):
        self.count += 1
        for player in self.players:
            player.prev_pos = math.pos(player.cur_pos)
            direction_vector = player.process_inputs()
            if direction_vector['y'] != 0:

                print 'Direction vector = {}'.format(direction_vector)
            player.pos = math.add_vector(player.prev_pos, direction_vector)
            player.check_bounds()
            player.cur_pos = math.pos(player.pos)
            if self.count % 2000 == 0:
                print 'Physics Iteration: {} >> Player {} current position: {}'.format(self.count, player.player_name, player.pos)

        if self.count % 2000 == 0:
            print 'Player count = {}'.format(len(self.players))
