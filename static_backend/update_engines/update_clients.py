from backend_channel import channel

__author__ = 'RookY2K'


class UpdateClients:
    def __init__(self, players, game_timer, ball):
        self.players = players
        self.ball = ball
        self.game_timer = game_timer
        self.last_left_seq = 0
        self.last_right_seq = 0
        self.count = 0

    def update(self):

        server_time = self.game_timer.timer_time
        self.count += 1
        left_pos = {}
        right_pos = {}
        left_seq = right_seq = -1
        for player in self.players:
            if player.side == 'left':
                left_pos = player.pos
                left_seq = player.last_input_seq
            elif player.side == 'right':
                right_pos = player.pos
                right_seq = player.last_input_seq

        msg = {
            'state': 'server-update',
            'left_pos': left_pos,
            'right_pos': right_pos,
            'left_seq': left_seq,
            'right_seq': right_seq,
            'ball_pos': self.ball.pos,
            'server_time': server_time
        }

        for player in self.players:
            channel.send_message_to_client(msg, player.token)