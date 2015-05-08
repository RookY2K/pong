#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from controllers import index, pong
from channel import channel


app = webapp2.WSGIApplication([
    ('/', index.Index),
    ('/login', index.Login),
    ('/lobby-update', index.Lobby),
    ('/pong', pong.Pong),
    ('/connect', channel.Connect),
    ('/open', channel.Open),
    ('/_ah/channel/disconnected/', pong.LeaveGame),
    ('/leave_game', pong.LeaveGame)
], debug=True)
