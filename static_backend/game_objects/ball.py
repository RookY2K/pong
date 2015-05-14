__author__ = 'Vince Maiuri'
from game_helpers import constants
from game_helpers import math
import time


class Ball:
    def __init__(self):
        self.radius = constants.BALL_RADIUS
        self.vel = {
            'x': 5,
            'y': 3
        }
        self.pos = {
            'x': constants.CANVAS_WIDTH / 2,
            'y': constants.CANVAS_HEIGHT / 2
        }
        self.prev_pos = math.pos(self.pos)
        self.cur_pos = math.pos(self.pos)
        self.time_stamp = time.time() * 1000
        self.limits = {
            'min_x': 0,
            'min_y': 0,
            'max_x': constants.CANVAS_WIDTH - self.radius,
            'max_y': constants.CANVAS_HEIGHT - self.radius
        }

    def check_bounds(self, players):
        if self.pos['y'] > self.limits['max_y']:
            self.pos['y'] = self.limits['max_y']
            self.vel['y'] = -self.vel['y']

        if self.pos['y'] < self.limits['min_y']:
            self.pos['y'] = self.limits['min_y']
            self.vel['y'] = -self.vel['y']

        for player in players:
            collision = self.check_paddle_collide(player)
            if collision:
                self.vel['x'] = -self.vel['x']

    def check_paddle_collide(self, player):
        if self.pos['x'] - self.radius > player.pos['x'] + player.width:
            return False

        if self.pos['x'] + self.radius < player.pos['x']:
            return False

        if self.pos['y'] - self.radius > player.pos['y'] + player.height:
            return False

        if self.pos['y'] + self.radius < player.pos['y']:
            return False

        return True