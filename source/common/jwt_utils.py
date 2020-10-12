import jwt
from taki_exception import TakiException
from codes import Status


SECRET_KEY = 'my_secret_key'  # TODO: move to config.py


def encode_player_jwt(game_id, player_name, is_host):
    return jwt.encode(
        {
            'game_id': game_id,
            'player_name': player_name,
            'is_host': is_host
        },
        SECRET_KEY,
        algorithm='HS256'
    )


def decode_player_jwt(player_jwt):
    try:
        return jwt.decode(player_jwt, SECRET_KEY, algorithm='HS256')
    except Exception:
        raise TakiException(Status.BAD_REQUEST, 'Invalid JWT.')
