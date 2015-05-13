__author__ = 'Vince Maiuri'

import json
from google.appengine.api import channel


def send_message_to_client(msg, token):
    channel.send_message(token, json.dumps(msg))