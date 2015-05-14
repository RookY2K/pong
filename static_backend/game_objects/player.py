__author__ = 'Vince Maiuri'
from game_helpers import constants
from game_helpers import math
import time


class Player:
    def __init__(self, player_name, side, game_index, token):
        self.length = constants.PADDLE_LENGTH
        self.width = constants.PADDLE_WIDTH
        self.player_name = player_name
        self.token = token
        self.side = side
        self.changed = False
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

    def check_bounds(self):
        if self.side == 'left' or self.side == 'right':
            if self.pos['y'] > self.limits['max_y']:
                self.pos['y'] = self.limits['max_y']

            if self.pos['y'] < self.limits['min_y']:
                self.pos['y'] = self.limits['min_y']

    def process_inputs(self):
        x_direction = y_direction = 0
        process_input = None
        input_length = len(self.inputs)

        if input_length:
            print 'Player {} inputs length = {}'.format(self.player_name, input_length)
            for i in range(input_length):
                process_input = self.inputs[i]
                print 'Input seq = {} and last input seq = {}'.format(process_input['seq'], self.last_input_seq)
                if process_input['seq'] <= self.last_input_seq:
                    continue

                inputs = process_input['inputs']
                length = len(inputs)

                for j in range(length):
                    single_input = inputs[j]
                    if single_input == 'up':
                        y_direction -= 1
                    elif single_input == 'down':
                        y_direction += 1

        vector = math.get_direction_vector(x_direction, y_direction)

        if process_input:
            self.last_input_time = process_input['time']
            self.last_input_seq = process_input['seq']
            del self.inputs[:input_length]

        return vector