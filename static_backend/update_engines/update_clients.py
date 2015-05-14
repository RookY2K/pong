from backend_channel import channel

__author__ = 'Vince Maiuri'


class UpdateClients:
    def __init__(self, players, game_timer):
        self.players = players
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

        if self.count % 4000 == 0:
            print 'Client update iteration: {} left pos = {}, right pos = {}, left seq = {}, right seq = {}'.format(self.count, left_pos, right_pos, left_seq, right_seq)

        msg = {
            'state': 'server-update',
            'left_pos': left_pos,
            'right_pos': right_pos,
            'left_seq': left_seq,
            'right_seq': right_seq,
            'server_time': server_time
        }
        update = False

        if left_seq > self.last_left_seq:
            self.last_left_seq = left_seq
            update = True

        if right_seq > self.last_right_seq:
            self.last_right_seq = right_seq
            update = True

        if update:
            for player in self.players:
                print 'Updating player {} with left pos: {}, right pos: {}, left seq: {}, and right seq: {}'.format(player.player_name, left_pos, right_pos, left_seq, right_seq)
                channel.send_message_to_client(msg, player.token)