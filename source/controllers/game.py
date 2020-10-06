from controller import controller
from ..common import validator, encode_player_jwt, Request, Response, Code, Status, Rule
from ..games import create_game, join_game


@controller(Code.CREATE_GAME)
@validator(Rule.CREATE_GAME)
def create_game_controller(args):
    lobby_name = str(args['lobby_name'])
    host = str(args['player_name'])
    password = str(args['password'])

    try:
        game = create_game(lobby_name, host, password)
    except:
        # handle no available lobbies
        pass

    print '[+] %s created game %s successfully' % (host, lobby_name)

    return Response(Status.SUCCESS, game_id = game.id, jwt = encode_player_jwt(game.id, host, True))


@controller(Code.JOIN_GAME)
@validator(Rule.JOIN_GAME)
def join_game_controller(args):
    game_id = args['game_id']
    player_name = str(args['player_name'])
    password = str(args['password'])

    try:
        join_game(player_name, game_id, password)
    except:
        # handle custom error
        pass
    
    print '[+] %s joined game %d successfully' % (player_name, game_id)

    return Response(Status.SUCCESS, jwt = encode_player_jwt(game_id, player_name, False))
