import json
import webapp2

__author__ = 'Vince Maiuri'

global_game_players = {}


class Input(webapp2.RequestHandler):
    def post(self):
        player_input = self.request.get('input')
        player_name = self.request.get('playerName')
        player = global_game_players[player_name]

        if player_input:
            inputs = json.loads(player_input)
            player.inputs.append({
                'inputs': inputs['inputs'],
                'time': inputs['time'],
                'seq': inputs['seq']
            })
            # print inputs['inputs']
            self.response.http_status_message(200)
        else:
            self.response.http_status_message(404)


def remove_player_inputs(player_name):
    del global_game_players[player_name]