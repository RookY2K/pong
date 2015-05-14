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
            player.pos = math.add_vector(player.prev_pos, direction_vector)
            player.check_bounds()
            player.cur_pos = math.pos(player.pos)

        self.ball.prev_pos = math.pos(self.ball.cur_pos)
        direction_vector = self.ball.vel
        self.ball.pos = math.add_vector(self.ball.prev_pos, direction_vector)
        self.ball.check_bounds(self.players)
        self.ball.cur_pos = math.pos(self.ball.pos)
