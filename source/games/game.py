MAX_PLAYERS = 4


class Game(object):
    def __init__(self, game_id, name, password, host):
        self.id = game_id
        self.name = name
        self.password = password
        self.host = host
        self.started = False
        self.players = [host]


    def add_player(self, player_name, password):
        if self.started:
            raise Exception('Game already started.') # should be a custom error

        if len(self.players) == MAX_PLAYERS:
            raise Exception('Game full.') # should be a custom error

        if self.already_joined(player_name):
            raise Exception('A player with this name already joined.') # should be a custom error

        if self.password != password:
            raise Exception('Invalid password.') # should be a custom error

        self.players.append(player_name)

    
    def already_joined(self, player_name):
        return player_name in self.players
