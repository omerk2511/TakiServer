from random import randint
from ..common import TakiException, Status


MIN_ID = 0
MAX_ID = 9999

in_use = []
# TODO: remove game from in_use on close


def get_game_id():
    if len(in_use) == MAX_ID - MIN_ID + 1:
        raise TakiException(Status.DENIED, 'No game ID available.')

    game_id = randint(MIN_ID, MAX_ID)
    while game_id in in_use:
        game_id = randint(MIN_ID, MAX_ID)

    in_use.append(game_id)

    return game_id
