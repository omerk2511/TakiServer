CARD_STRUCTURE = {"type": "", "color": "", "value": ""}


class Rule(object):
    CREATE_GAME = [
        ('lobby_name', lambda lobby_name: type(lobby_name) in (
            str, unicode) and str(lobby_name).strip() != ''),
        ('player_name', lambda player_name: type(player_name)
         in (str, unicode) and str(player_name).strip() != ''),
        ('password', lambda password: type(password) in (str, unicode))
    ]

    JOIN_GAME = [
        ('game_id', lambda game_id: type(game_id) is int),
        ('player_name', lambda player_name: type(player_name)
         in (str, unicode) and str(player_name).strip() != ''),
        ('password', lambda password: type(password) in (str, unicode))
    ]

    PLACE_CARDS = [
        ('cards', lambda cards: all(card.viewkeys() == CARD_STRUCTURE.viewkeys() for card in cards))
    ]
