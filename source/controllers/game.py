from controller import controller
from ..common import validator, encode_player_jwt, Response, Code, \
    Status, Rule, Responses, TakiException, authenticated
from ..games import create_game, join_game, leave_game, start_game

@controller(Code.CREATE_GAME)
@validator(Rule.CREATE_GAME)
def create_game_controller(args, client):
    lobby_name = str(args['lobby_name']).strip()
    host = str(args['player_name']).strip()
    password = str(args['password']).strip()
    if not client.in_game:
        try:
            game = create_game(lobby_name, password, host, client)
            client.in_game = True
        except TakiException as e:
            return e.response()
        except Exception as e:
            return Responses.INTERNAL_ERROR
    else:
        return Responses.BAD_REQUEST 
    print '[+] %s created game %s successfully' % (host, game.id)

    return Response(Status.SUCCESS, game_id=game.id, jwt=encode_player_jwt(
        game.id, host, True))


@controller(Code.JOIN_GAME)
@validator(Rule.JOIN_GAME)
def join_game_controller(args, client):
    game_id = args['game_id']
    player_name = str(args['player_name']).strip()
    password = str(args['password']).strip()
    if not client.in_game:
        try:
            join_game(player_name, game_id, password, client)
            client.in_game = True
        except TakiException as e:
            return e.response()
        except Exception:
            return Responses.INTERNAL_ERROR
    else:
        return Responses.BAD_REQUEST 

    print '[+] %s joined game %d successfully' % (player_name, game_id)

    return Response(Status.SUCCESS,
                    jwt=encode_player_jwt(game_id, player_name, False))


@controller(Code.LEAVE_GAME)
@authenticated
def leave_game_controller(user, args, sock):
    try:
        leave_game(str(user['player_name']).strip(), user['game_id'])
    except TakiException as e:
        return e.response()
    except Exception:
        return Responses.INTERNAL_ERROR

    print '[+] %s left game %d successfully' % (user['player_name'], user['game_id'])

    return Response(Status.SUCCESS)


@controller(Code.START_GAME)
@authenticated
def start_game_controller(user, args, client):
    if not user['is_host']:
        return Response(Status.DENIED,
                        message='You are not the administrator of the lobby.')

    try:
        start_game(user['game_id'])
    except TakiException as e:
        return e.response()
    except Exception:
        return Responses.INTERNAL_ERROR

    print '[+] game %d started successfully' % (user['game_id'])

    return Response(Status.SUCCESS)
