from game import Game
from utils import get_game_id


games = {}


def create_game(name, password, host):
    game = Game(get_game_id(), name, password, host)
    games[game.id] = game
    
    return game


def join_game(player_name, game_id, password):
    if game_id not in games:
        raise Exception('Game id not found.') # should be a custom error

    game = games[game_id]
    game.add_player(player_name, password)
    