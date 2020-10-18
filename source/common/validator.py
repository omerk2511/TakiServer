import functools
from jwt_utils import decode_player_jwt
from taki_exception import TakiException
from message import Response
from codes import Status
from responses import Responses

RULE_NAME = 0
RULE_CALLBACK = 1


def validate_args(args, rules):
    if type(args) != dict:
        return False

    for rule in rules:
        if rule[RULE_NAME] not in args or \
                not rule[RULE_CALLBACK](args[rule[RULE_NAME]]):
            return False

    return True


def validator(rules):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(args, client):
            if validate_args(args, rules):
                return func(args, client)

            raise ValueError('Invalid request.')

        return wrapper

    return decorator


def authenticated(func):
    @functools.wraps(func)
    def wrapper(args, client):
        try:
            user = decode_player_jwt(args['jwt'])
            del args['jwt']
            return func(user, args, client)
        except TakiException as e:
            return e.response()
        except Exception:
            return Response(Status.BAD_REQUEST, message='No JWT supplied.')

    return wrapper


def not_in_game(func):
    @functools.wraps(func)
    def wrapper(args, client):
        if client.in_game:
            return Responses.BAD_REQUEST

        return func(args, client)

    return wrapper
