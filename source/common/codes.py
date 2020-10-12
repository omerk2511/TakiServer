class Code(object):
    # Server Broadcast Messages Codes
    PLAYER_JOINED = 'player_joined'
    PLAYER_LEFT = 'player_left'
    GAME_STARTING = 'game_starting'
    UPDATE_TURN = 'update_turn'
    MOVE_DONE = 'move_done'
    PLAYER_WON = 'player_won'
    GAME_ENDED = 'game_ended'

    # Requests Codes
    CREATE_GAME = 'create_game'
    JOIN_GAME = 'join_game'
    LEAVE_GAME = 'leave_game'
    START_GAME = 'start_game'
    PLACE_CARDS = 'place_cards'
    TAKE_CARDS = 'take_cards'


class Status(object):
    # General Statuses
    SUCCESS = 'success'
    BAD_REQUEST = 'bad_request'
    DENIED = 'denied'
    NOT_FOUND = 'not_found'
    CONFLICT = 'conflict'
    INTERNAL_ERROR = 'internal_error'
