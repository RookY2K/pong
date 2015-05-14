__author__ = 'Vince Maiuri'

import webapp2
from server import server, inputs
from backend_channel import channel


app = webapp2.WSGIApplication([
    ('/game/start', server.Start),
    ('/game/inputs', inputs.Input),
    ('/game/connect', channel.Connect),
    ('/game/open', channel.Open),
    ('/_ah/channel/disconnected/', channel.LeaveGame),
    ('/game/leave_game', channel.LeaveGame)
], debug=True)
