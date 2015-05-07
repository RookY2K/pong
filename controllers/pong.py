__author__ = 'Vince Maiuri'

import webapp2

from helpers import constants

class Pong(webapp2.RequestHandler):
    def get(self):
        player_name = self.request.get('playerName')
        game_id = self.request.get('gameId')

        template_values = {
            'player_name': player_name,
            'game_id': game_id
        }

        template = constants.JINJA_ENVIRONMENT.get_template('pong.html')
        self.response.write(template.render(template_values))
