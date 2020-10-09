from ..common import TakiException, Status, Request, Code

MAX_PLAYERS = 4


class Game(object):
    def __init__(self, game_id, name, password, host, sock):
        self.id = game_id
        self.name = name
        self.password = password
        self.host = host
        self.started = False
        self.players = [host]
        self.sockets = [sock]
        # TODO: add a lock

    def add_player(self, player_name, password, sock):
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
        self.broadcast(Request(Code.PLAYER_JOINED, player_name=player_name))
        self.sockets.append(sock)

    def remove_player(self, player_name):
        if not self.player_joined(player_name):
            raise TakiException(Status.BAD_REQUEST,
                                'This player is not in the game lobby.')

        del self.sockets[self.players.index(player_name)]
        self.players.remove(player_name)

        if player_name == self.host:
            pass  # TODO: close game and broadcast
        else:
            self.broadcast(Request(Code.PLAYER_LEFT, player_name=player_name))

    def start(self):
        if len(self.players) != MAX_PLAYERS:
            raise TakiException(Status.DENIED, 'The game lobby is not full.')

        self.started = True
        self.broadcast(Request(Code.GAME_STARTING, players=self.players))
        # TODO: add card generation

    def player_joined(self, player_name):
        return player_name in self.players

    def broadcast(self, message):
        for sock in self.sockets:
            sock.send(message.serialize())
