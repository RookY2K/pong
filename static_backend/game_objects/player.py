__author__ = 'Vince Maiuri'
from static_backend.game_helpers import constants
from static_backend.game_helpers import math
import time


class Player:
    def __init__(self, user_name, side, game_index, token):
        self.length = constants.PADDLE_LENGTH
        self.width = constants.PADDLE_WIDTH
        self.user_name = user_name
        self.token = token
        self.side = side
        self.game_index = game_index
        if self.side == 'left':
            self.pos = {'x': 10, 'y': constants.CANVAS_HEIGHT/2 - self.length/2}
        elif self.side == 'right':
            self.pos = {'x': constants.CANVAS_WIDTH - 10, 'y': constants.CANVAS_HEIGHT/2 - self.length/2}
        self.prev_pos = math.pos(self.pos)
        self.cur_pos = math.pos(self.pos)
        self.time_stamp = time.time() * 1000
        self.inputs = []
        self.limits = {
            'min_x': 0,
            'min_y': 0,
            'max_x': constants.CANVAS_WIDTH - self.length,
            'max_y': constants.CANVAS_HEIGHT - self.length
        }
        self.last_input_seq = 0
        self.last_input_time = self.time_stamp