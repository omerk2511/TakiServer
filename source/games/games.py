from game import Game
from utils import get_game_id
from ..common import TakiException, Status


games = {}


def create_game(name, password, host, sock):
    game = Game(get_game_id(), name, password, host, sock)
    games[game.id] = game

    return game


def join_game(player_name, game_id, password, sock):
    if game_id not in games:
        raise TakiException(Status.NOT_FOUND,
                            'A game with the supplied game ID was not found.')

    game = games[game_id]
    game.add_player(player_name, password, sock)


def leave_game(player_name, game_id):
    if game_id not in games:
        raise TakiException(Status.NOT_FOUND,
                            'A game with the supplied game ID was not found.')

    game = games[game_id]
    game.remove_player(player_name)


def start_game(game_id):
    if game_id not in games:
        raise TakiException(Status.NOT_FOUND,
                            'A game with the supplied game ID was not found.')

    game = games[game_id]
    game.start()
