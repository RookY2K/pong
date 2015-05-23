__author__ = 'RookY2K'
import time


class UpdateTimer:
    def __init__(self):
        self.timer_time = .016
        self.count = 0
        self.timer_start_delta = time.time() * 1000
        self.timer_end_delta = time.time() * 1000

    def update_timer(self):
        self.timer_start_delta = (time.time() * 1000) - self.timer_end_delta
        self.timer_end_delta = time.time() * 1000
        self.count += 1
        self.timer_time += self.timer_start_delta / 1000.0