__author__ = 'RookY2K'


from google.appengine.ext import ndb
from google.appengine.api import memcache
from game_helpers import constants
from backend_models.player import Player


class Game(ndb.Model):
    game_index = ndb.StringProperty(required=True, indexed=True)
    num_players = ndb.IntegerProperty(required=True, default=0)
    ready = ndb.IntegerProperty(required=True, default=0)
    players = ndb.StringProperty(repeated=True)

    _default_parent = 'pong_parent'

    @classmethod
    def _game_parent_key(cls, parent_name=_default_parent):
        return ndb.Key('Pong', parent_name)

    @classmethod
    def _game_key(cls, game_index, parent_name=_default_parent):
        return ndb.Key('Game', game_index, parent=cls._game_parent_key(parent_name))

    @ndb.transactional()
    def incr_ready(self):
        self.ready += 1
        self.put()
        memcache.set(self.game_index, self)

        return self.ready

    @ndb.transactional(xg=True)
    def add_player(self, player_name):
        if self.num_players < constants.MAX_PLAYERS:
            if self.num_players == 0:
                players = []
            else:
                players = self.players
            self.num_players += 1
            players.append(player_name)

            player = Player.get_player(player_name)
            if not player.add_game(self.game_index):
                return False

            self.players = players
            self.put()
            memcache.set(self.game_index, self)
            return True
        else:
            return False

    @ndb.transactional(xg=True)
    def remove_player(self, player_name):
        if player_name not in self.players:
            return False

        self.players.remove(player_name)
        self.num_players -= 1
        self.ready -= 1

        player = Player.get_player(player_name)
        player.clear_game()

        self.put()
        memcache.set(self.game_index, self)
        return True

    @classmethod
    def get_game(cls, game_index):
        try:
            game = memcache.get(game_index)
        except ImportError:
            game = None

        if not game:
            game_key = cls._game_key(game_index)
            game = game_key.get()
            memcache.set(game.game_index, game)

        return game

    @classmethod
    @ndb.transactional()
    def get_all_games(cls):
        games = cls._get_games_from_memcache()

        if not games:
            game_query = cls.query(ancestor=cls._game_parent_key()).order(cls.game_index)
            games = game_query.fetch(constants.MAX_GAMES)
            if not games:
                games = cls._create_all_games()

            game_range = [str(x) for x in range(1, constants.MAX_GAMES+1)]
            game_dict = {}
            for i in range(len(games)):
                game_dict[str(game_range[i])] = games[i]

            memcache.set_multi(game_dict, key_prefix='game-')

        return games

    @classmethod
    def _get_games_from_memcache(cls):
        games = None
        game_range = [str(x) for x in range(1, constants.MAX_GAMES+1)]
        try:
            games_dict = memcache.get_multi(game_range, key_prefix='game-')
        except ImportError:
            games_dict = None

        if games_dict:
            games = []
            for key, value in games_dict.iteritems():
                games.append(value)

            games = sorted(games, key=lambda game: game.game_index)

        return games

    @classmethod
    def _create_all_games(cls):
        games = []
        for i in range(constants.MAX_GAMES):
            index = 'game-{}'.format(i+1)
            game = cls(
                key=cls._game_key(index),
                game_index=index)
            games.append(game)
        ndb.put_multi(games)
        return games