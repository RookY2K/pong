__author__ = 'Vince Maiuri'

import json
from google.appengine.api import channel


def send_message_to_client(msg, player):
    channel.send_message(player.token, json.dumps(msg))