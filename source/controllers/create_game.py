from controller import controller
from ..common import Message, Request, Response

# move to responses/
CREATE_GAME = {
    "status": "success",
    "args": {
        "game_id":  "",
        "jwt":      ""
    }
}


@controller('create_game')
def create_game(args):
    status = 'success'
    lobby_name = args['lobby_name']
    host = args['player_name']
    password = args['password']
    print ("[+] %s created lobby '%s'") % (host,lobby_name)
    return Response(status,{'game_id': '1', 'jwt': 'RND'})
