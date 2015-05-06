__author__ = 'Vince Maiuri'


from google.appengine.ext import ndb
from helpers import constants


class Game(ndb.Model):
    game_index = ndb.StringProperty(required=True, indexed=True)
    num_players = ndb.IntegerProperty(required=True, default=0)
    players = ndb.JsonProperty(repeated=True)

    default_parent = 'pong_parent'

    @classmethod
    def game_parent_key(cls, parent_name=default_parent):
        return ndb.Key('Pong', parent_name)

    @ndb.transactional()
    def add_player(self, player):
        if self.num_players < constants.MAX_PLAYERS:
            if self.num_players == 0:
                players = []
            else:
                players = self.players
            self.num_players += 1
            players.append(player)
            self.players = players
            self.put()
            return True
        else:
            return False

    @classmethod
    def get_game(cls, game_index):
        game_query = cls.query(
            ancestor=cls.game_parent_key(),
            game_index=game_index
        )
        return game_query.fetch(1)[0]

    @classmethod
    @ndb.transactional()
    def get_all_games(cls):
        game_query = cls.query(ancestor=cls.game_parent_key()).order(cls.game_index)
        games = game_query.fetch(constants.MAX_GAMES)
        if not games:
            games = cls.create_all_games()

        return games

    @classmethod
    def create_all_games(cls):
        games = []
        for i in range(constants.MAX_GAMES):
            index = 'game-{}'.format(i+1)
            game = cls(
                parent=cls.game_parent_key(),
                game_index=index)
            games.append(game)
        ndb.put_multi(games)
        return games