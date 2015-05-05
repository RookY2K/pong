__author__ = 'Vince Maiuri'

import webapp2
from server import server


app = webapp2.WSGIApplication([
    ('/_ah/start', server.Start)
], debug=True)
