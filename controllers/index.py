__author__ = 'Vince Maiuri'
import webapp2

from helpers.constants import *


class Index(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('pong.html')
        self.response.write(template.render())
