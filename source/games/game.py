from ..common import TakiException, Status

MAX_PLAYERS = 4


class Game(object):
    def __init__(self, game_id, name, password, host):
        self.id = game_id
        self.name = name
        self.password = password
        self.host = host
        self.started = False
        self.players = [host]

    def add_player(self, player_name, password):
        if self.started:
            raise TakiException(Status.DENIED, 'The game has already started.')

        if len(self.players) == MAX_PLAYERS:
            raise TakiException(Status.DENIED, 'The game lobby is full.')

        if self.player_joined(player_name):
            raise TakiException(Status.CONFLICT,
                                'The chosen name is already taken.')

        if password != self.password:
            raise TakiException(Status.DENIED, 'Invalid password.')

        self.players.append(player_name)
        # TODO: broadcast

    def remove_player(self, player_name):
        if not self.player_joined(player_name):
            raise TakiException(Status.BAD_REQUEST,
                                'This player is not in the game lobby.')

        self.players.remove(player_name)
        # TODO: broadcast, handle host / regular player cases

    def start(self):
        if len(self.players) != MAX_PLAYERS:
            raise TakiException(Status.DENIED, 'The game lobby is not full.')
            # TODO: broadcast

        self.started = True

    def player_joined(self, player_name):
        return player_name in self.players
