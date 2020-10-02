from controller import controller
from ..common import Request, Response, Codes


@controller(Codes.CREATE_GAME)
def create_game(args):
    status = Codes.SUCCESS
    lobby_name = args['lobby_name']
    host = args['player_name']
    password = args['password']
    print ('[+] %s created lobby %s successfully') % (host, lobby_name)
    return Response(status, game_id = 'RND', jwt = 'RND')
