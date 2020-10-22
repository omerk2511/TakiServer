from ..common import TakiException, Status, Request, Code
from ..cards import Card, Deck, CardType, valid_move
from threading import Lock
import random

MAX_PLAYERS = 4


class Game(object):
    def __init__(self, game_id, name, password, host, client, games):
        self.id = game_id
        self.name = name
        self.password = password
        self.host = host
        self.started = False
        self.players = [{
            'name': host,
            'client': client
        }]
        self.game_lock = Lock()
        self.deck = Deck()
        self.current_player = 0
        self.plus_2_count = 0
        self.plus_2_active = False
        self.last_card = Card(None, '', '')
        self.direction = 1
        self.scoreboard = []
        self.games = games

    def add_player(self, player_name, password, client):
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
                'client': client
            }

            self.players.append(player)

    def remove_player(self, player_name):
        if not self.player_joined(player_name):
            raise TakiException(Status.BAD_REQUEST,
                                'This player is not in the game lobby.')

        if self.started:
            raise TakiException(Status.BAD_REQUEST,
                                'The game has already started.')

        with self.game_lock:
            player = self.find_player(player_name)

            self.players[player]['client']._in_game = False
            del self.players[player]

        self.broadcast(Request(Code.PLAYER_LEFT, player_name=player_name))

        if player_name == self.host:
            self.broadcast(Request(Code.GAME_ENDED, scoreboard=[]))

            for player in self.players:
                player['client']._in_game = False

            del self.games[self.id]

    def start(self):
        if len(self.players) != MAX_PLAYERS:
            raise TakiException(Status.DENIED, 'The game lobby is not full.')

        self.started = True
        self.shuffle_players()

        self.active_players = self.players[:]

        for i, player in enumerate(self.players):
            player_names = [p['name'] for p in (
                self.players[i:] + self.players[:i])]

            player['hand'] = self.deck.get_hand()
            player['client']._socket.send(Request(Code.GAME_STARTING,
                                          players=player_names,
                                          cards=[card.serialize() for card in player['hand'].cards]
                                          ).serialize())

        self.update_turn()

    def take_cards(self, player_name):
        if self.current_player != self.find_active_player(player_name):
            raise TakiException(Status.DENIED, 'It\'s not your turn.')

        self.deck.shuffle()

        count = 1 if not self.plus_2_count else self.plus_2_count
        cards = self.deck.get_random_cards(count)

        self.active_players[self.find_active_player(player_name)]['hand'].append_cards(cards)
        self.broadcast(Request(Code.MOVE_DONE, type='cards_taken',
                               amount=count, player_name=player_name))

        self.plus_2_count = 0
        self.plus_2_active = False

        self.current_player = (self.current_player + self.direction) % len(self.active_players)
        self.update_turn()

        return cards

    def place_cards(self, player_name, raw_cards):
        if self.current_player != self.find_active_player(player_name):
            raise TakiException(Status.DENIED, 'It\'s not your turn.')

        if len(raw_cards) == 0:
            raise TakiException(Status.BAD_REQUEST, 'You must supply at least one card.')

        cards = [Card.deserialize(raw_card) for raw_card in raw_cards]

        player = self.find_active_player(player_name)
        hand = self.active_players[player]['hand']

        first = True
        stop_done = False
        in_taki = False
        last_card = self.last_card

        for card in cards:
            if not hand.card_exists(card, cards.count(card)) or \
                    not valid_move(card, last_card, first, in_taki, self.plus_2_active):
                raise TakiException(Status.BAD_REQUEST, 'Invalid move done.')

            if card.type == CardType.STOP:
                stop_done = True

            if card.type == CardType.TAKI or card.type == CardType.SUPER_TAKI:
                in_taki = True

            first = False
            last_card = card

        for card in cards:
            if card.type == CardType.PLUS_2:
                self.plus_2_count += 2
                self.plus_2_active = True

            if card.type == CardType.CHANGE_DIRECTION:
                self.direction = -self.direction

            hand.remove_card(card)

            new_card = Card(card.type, card.color, card.value)

            if card.type == CardType.SUPER_TAKI or card.type == CardType.CHANGE_COLOR:
                new_card.color = ''

            self.deck.add_card(new_card)

        self.last_card = last_card

        self.broadcast(Request(Code.MOVE_DONE, type='cards_placed',
                               cards=raw_cards, player_name=player_name))

        if hand.empty():
            if player == len(self.active_players) - 1:
                self.current_player = 0

            self.player_finished(player_name)
        else:
            self.current_player = (self.current_player + (int(stop_done) + 1) * self.direction) % len(self.active_players)

        self.update_turn()

    def update_turn(self):
        self.broadcast(Request(Code.UPDATE_TURN,
                               current_player=self.active_players[
                                   self.current_player]['name']))

    def player_joined(self, player_name):
        with self.game_lock:
            return self.find_player(player_name) is not None

    def find_player(self, player_name):
        return next((i for i, player in enumerate(self.players)
                    if player['name'] == player_name), None)

    def find_active_player(self, player_name):
        return next((i for i, player in enumerate(self.active_players)
                    if player['name'] == player_name), None)

    def shuffle_players(self):
        random.shuffle(self.players)

    def player_finished(self, player_name):
        self.broadcast(Request(Code.PLAYER_FINISHED, player_name=player_name))

        self.scoreboard.append(player_name)
        del self.active_players[self.find_active_player(player_name)]

        if len(self.scoreboard) == len(self.players) - 1:
            last_name = self.active_players[0]['name']

            self.broadcast(Request(Code.PLAYER_FINISHED, player_name=last_name))
            self.scoreboard.append(last_name)

            self.broadcast(Request(Code.GAME_ENDED, scoreboard=self.scoreboard))

            for player in self.players:
                player['client']._in_game = False

            del self.games[self.id]

    def broadcast(self, message):
        with self.game_lock:
            for player in self.players:
                player['client']._socket.send(message.serialize())
