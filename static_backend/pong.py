__author__ = 'Vince Maiuri'

import webapp2
from server import server


app = webapp2.WSGIApplication([
    ('/game/start', server.Start)
], debug=True)
