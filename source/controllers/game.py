from controller import controller
from ..common import validator, encode_player_jwt, Response, Code, \
    Status, Rule, Responses, TakiException, authenticated, not_in_game
from ..games import create_game, join_game, leave_game, start_game, \
    take_cards, place_cards


@controller(Code.CREATE_GAME)
@validator(Rule.CREATE_GAME)
@not_in_game
def create_game_controller(args, client):
    lobby_name = str(args['lobby_name']).strip()
    host = str(args['player_name']).strip()
    password = str(args['password']).strip()

    try:
        game = create_game(lobby_name, password, host, client)

        client._in_game = True
        client._game_id = game.id
        client._player_name = host
    except TakiException as e:
        return e.response()
    except Exception as e:
        print '[-]', e
        return Responses.INTERNAL_ERROR

    print '[+] %s created game %s successfully' % (host, game.id)

    return Response(Status.SUCCESS, game_id=game.id, jwt=encode_player_jwt(
        game.id, host, True))


@controller(Code.JOIN_GAME)
@validator(Rule.JOIN_GAME)
@not_in_game
def join_game_controller(args, client):
    game_id = args['game_id']
    player_name = str(args['player_name']).strip()
    password = str(args['password']).strip()

    try:
        game = join_game(player_name, game_id, password, client)

        client._in_game = True
        client._game_id = game.id
        client._player_name = player_name
    except TakiException as e:
        return e.response()
    except Exception as e:
        print '[-]', e
        return Responses.INTERNAL_ERROR

    print '[+] %s joined game %d successfully' % (player_name, game_id)

    return Response(Status.SUCCESS,
                    jwt=encode_player_jwt(game_id, player_name, False),
                    players=[p['name'] for p in game.players])


@controller(Code.LEAVE_GAME)
@authenticated
def leave_game_controller(user, args, sock):
    try:
        leave_game(str(user['player_name']).strip(), user['game_id'])
    except TakiException as e:
        return e.response()
    except Exception as e:
        print '[-]', e
        return Responses.INTERNAL_ERROR

    print '[+] %s left game %d successfully' % (user['player_name'],
                                                user['game_id'])

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
    except Exception as e:
        print '[-]', e
        return Responses.INTERNAL_ERROR

    print '[+] game %d started successfully' % (user['game_id'])

    return Response(Status.SUCCESS)


@controller(Code.TAKE_CARDS)
@authenticated
def take_cards_controller(user, args, sock):
    try:
        cards = take_cards(str(user['player_name']).strip(), user['game_id'])
    except TakiException as e:
        return e.response()
    except Exception as e:
        print '[-]', e
        return Responses.INTERNAL_ERROR

    return Response(Status.SUCCESS, cards=[card.serialize() for card in cards])


@controller(Code.PLACE_CARDS)
@validator(Rule.PLACE_CARDS)
@authenticated
def place_cards_controller(user, args, sock):
    try:
        place_cards(str(user['player_name']).strip(), args['cards'], user['game_id'])
    except TakiException as e:
        return e.response()
    except Exception as e:
        print '[-]', e
        return Responses.INTERNAL_ERROR

    return Response(Status.SUCCESS)
