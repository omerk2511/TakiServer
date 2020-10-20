from game import Game
from utils import get_game_id
from ..common import TakiException, Status


games = {}


def find_game(game_id):
    if game_id not in games:
        raise TakiException(Status.NOT_FOUND,
                            'A game with the supplied game ID was not found.')

    return games[game_id]


def create_game(name, password, host, sock):
    game = Game(get_game_id(), name, password, host, sock)
    games[game.id] = game

    return game


def join_game(player_name, game_id, password, sock):
    find_game(game_id).add_player(player_name, password, sock)


def leave_game(player_name, game_id):
    find_game(game_id).remove_player(player_name)


def start_game(game_id):
    find_game(game_id).start()


def take_cards(player_name, game_id):
    return find_game(game_id).take_cards(player_name)


def place_cards(player_name, raw_cards, game_id):
    return find_game(game_id).place_cards(player_name, raw_cards)
