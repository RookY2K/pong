__author__ = 'RookY2K'
from game_helpers import constants
from game_helpers import math
import time


class Ball:
    def __init__(self, game_id):
        self.radius = constants.BALL_RADIUS
        self.vel = {
            'x': .10,
            'y': .10
        }
        self.pos = {
            'x': constants.CANVAS_WIDTH / 2,
            'y': constants.CANVAS_HEIGHT / 2
        }
        self.game_id = game_id
        self.waiting = True
        self.won = None
        self.prev_pos = math.pos(self.pos)
        self.cur_pos = math.pos(self.pos)
        self.time_stamp = time.time() * 1000
        self.limits = {
            'min_x': -self.radius,
            'min_y': 0,
            'max_x': constants.CANVAS_WIDTH + self.radius,
            'max_y': constants.CANVAS_HEIGHT - self.radius
        }

    def check_bounds(self, players):
        if self.prev_pos['y'] > self.limits['max_y']:
            self.pos['y'] = self.limits['max_y']
            self.vel['y'] = -self.vel['y']

        if self.prev_pos['y'] < self.limits['min_y']:
            self.pos['y'] = self.limits['min_y']
            self.vel['y'] = -self.vel['y']

        if self.prev_pos['x'] > self.limits['max_x']:
            self.won = 'left'

        if self.prev_pos['x'] < self.limits['min_x']:
            self.won = 'right'

        for player in players:
            collision = self.check_paddle_collide(player)
            if collision:
                self.vel['x'] = -self.vel['x']
                if self.prev_pos['x'] > 500:
                    self.pos['x'] -= .5
                else:
                    self.pos['x'] += .5

    def check_paddle_collide(self, player):
        if self.prev_pos['x'] - self.radius > player.pos['x'] + player.width:
            return False

        if self.prev_pos['x'] + self.radius < player.pos['x']:
            return False

        if self.prev_pos['y'] - self.radius > player.pos['y'] + player.length:
            return False

        if self.prev_pos['y'] + self.radius < player.pos['y']:
            return False

        return True