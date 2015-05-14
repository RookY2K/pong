__author__ = 'Vince Maiuri'

from google.appengine.ext import ndb
from google.appengine.api import memcache


class Player(ndb.Model):
    name = ndb.StringProperty(required=True)
    game_id = ndb.StringProperty(default='')
    token = ndb.TextProperty(default='')
    high_score = ndb.IntegerProperty(required=True, default=0)

    _default_parent = 'player_parent'

    @classmethod
    def _parent_key(cls, parent_name=_default_parent):
        return ndb.Key('player_parent', parent_name)

    @classmethod
    def _player_key(cls, name, parent_name=_default_parent):
        return ndb.Key('Player', name.upper(), parent=cls._parent_key(parent_name))

    @classmethod
    @ndb.transactional()
    def get_player(cls, name):
        player = memcache.get(name)

        if not player:
            player_key = cls._player_key(name)
            player = player_key.get()

            if not player:
                player = cls._add_player(name)

            memcache.set(name, player)
        return player

    @classmethod
    def _add_player(cls, name):
        player = cls(
            key=cls._player_key(name),
            name=name
        )
        player.put()
        memcache.set(player.name, player)
        return player

    @classmethod
    def query_all(cls, parent_name=_default_parent):
        return cls.query(ancestor=cls._parent_key(parent_name)).order(-cls.high_score)


    @classmethod
    def paginate_players(cls, page):
        qry = cls.query_all()
        cursor = None
        this_page_cursor_key = "cursor_for_page_%s" % page
        next_page_cursor_key = "cursor_for_page_%s" % (page + 1)
        if page > 1:
            cursor = memcache.get(this_page_cursor_key)

        players, next_page_cursor, more = qry.fetch_page(10, start_cursor=cursor)
        memcache.set(next_page_cursor_key, next_page_cursor)

        return [players, more]

    @ndb.transactional()
    def set_highscore(self, score):
        self.high_score += score
        self.put()
        memcache.set(self.name, self)

    @ndb.transactional()
    def add_game(self, game_id):
        if self.game_id:
            return False

        self.game_id = game_id
        self.put()
        memcache.set(self.name, self)
        return True

    @ndb.transactional()
    def clear_game(self):
        self.game_id = ''
        self._clear_token()
        self.put()
        memcache.set(self.name, self)

    @ndb.transactional()
    def add_token(self, token):
        self.token = token
        self.put()
        memcache.set(self.name, self)

    @ndb.transactional()
    def _clear_token(self):
        self.token = ''
