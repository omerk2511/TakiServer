from ..common import TakiException, Status, Request, Code
from ..cards import Deck
from threading import Lock
import random

MAX_PLAYERS = 4


class Game(object):
    def __init__(self, game_id, name, password, host, sock):
        self.id = game_id
        self.name = name
        self.password = password
        self.host = host
        self.started = False
        self.players = [{
            'name': host,
            'socket': sock
        }]
        self.game_lock = Lock()
        self.deck = Deck()
        self.current_player = 0
        self.plus_2_count = 0

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

        self.broadcast(Request(Code.PLAYER_JOINED, player_name=player_name))

        with self.game_lock:
            player = {
                'name': player_name,
                'socket': sock
            }

            self.players.append(player)

    def remove_player(self, player_name):
        if not self.player_joined(player_name):
            raise TakiException(Status.BAD_REQUEST,
                                'This player is not in the game lobby.')

        with self.game_lock:
            del self.players[self.find_player(player_name)]

        if player_name == self.host:
            pass  # TODO: close game and broadcast
        else:
            self.broadcast(Request(Code.PLAYER_LEFT, player_name=player_name))

    def start(self):
        if len(self.players) != MAX_PLAYERS:
            raise TakiException(Status.DENIED, 'The game lobby is not full.')

        self.started = True
        self.shuffle_players()

        for i, player in enumerate(self.players):
            player_names = [p['name'] for p in (
                self.players[i:] + self.players[:i])]

            player['hand'] = self.deck.get_hand()
            player['socket'].send(Request(Code.GAME_STARTING,
                                          players=player_names,
                                          cards=player['hand'].cards
                                          ).serialize())

        self.broadcast(Request(Code.UPDATE_TURN,
                               current_player=self.players[
                                   self.current_player]['name']))

    def take_cards(self, player_name):
        count = 1 if not self.plus_2_count else self.plus_2_count
        cards = self.deck.get_random_cards(count)

        self.players[self.find_player(player_name)]['hand'].append_cards(cards)
        self.broadcast(Request(Code.MOVE_DONE, type='cards_taken',
                               amount=count, player_name=player_name))

        return cards

    def player_joined(self, player_name):
        with self.game_lock:
            return player_name in self.players

    def find_player(self, player_name):
        return next((i for i, player in enumerate(self.players)
                    if player['name'] == player_name), None)

    def shuffle_players(self):
        random.shuffle(self.players)

    def broadcast(self, message):
        with self.game_lock:
            for sock in self.sockets:
                sock.send(message.serialize())
