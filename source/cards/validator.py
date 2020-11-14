from card import Card
from card_type import CardType

FIRST_STATE_MACHINE = {
    CardType.NUMBER_CARD: lambda card, other, plus_2_active: card.color == other.color or card.value == other.value or other.type in (CardType.CHANGE_COLOR, CardType.SUPER_TAKI),
    CardType.PLUS: lambda card, other, plus_2_active: card.type == other.type or card.color == other.color or other.type in (CardType.CHANGE_COLOR, CardType.SUPER_TAKI),
    CardType.PLUS_2: lambda card, other, plus_2_active: card.type == other.type or (not plus_2_active and (card.color == other.color or other.type in (CardType.CHANGE_COLOR, CardType.SUPER_TAKI))),
    CardType.STOP: lambda card, other, plus_2_active: card.type == other.type or card.color == other.color or other.type in (CardType.CHANGE_COLOR, CardType.SUPER_TAKI),
    CardType.CHANGE_DIRECTION: lambda card, other, plus_2_active: card.type == other.type or card.color == other.color or other.type in (CardType.CHANGE_COLOR, CardType.SUPER_TAKI),
    CardType.CHANGE_COLOR: lambda card, other, plus_2_active: card.type == other.type or card.color == other.color or other.type in (CardType.CHANGE_COLOR, CardType.SUPER_TAKI),
    CardType.TAKI: lambda card, other, plus_2_active: card.type == other.type or card.color == other.color or other.type in (CardType.CHANGE_COLOR, CardType.SUPER_TAKI),
    CardType.SUPER_TAKI: lambda card, other, plus_2_active: card.type == other.type or other.type == CardType.TAKI or card.color == other.color or other.type in (CardType.CHANGE_COLOR, CardType.SUPER_TAKI),
    None: lambda card, other, plus_2_active: True
}

REGULAR_STATE_MACHINE = {
    CardType.NUMBER_CARD: lambda card, other, in_taki: in_taki and card.color == other.color,
    CardType.PLUS: lambda card, other, in_taki: card.type == other.type or card.color == other.color,
    CardType.PLUS_2: lambda card, other, in_taki: in_taki and card.color == other.color,
    CardType.STOP: lambda card, other, in_taki: in_taki and card.color == other.color,
    CardType.CHANGE_DIRECTION: lambda card, other, in_taki: in_taki and card.color == other.color,
    CardType.CHANGE_COLOR: lambda card, other, in_taki: False,
    CardType.TAKI: lambda card, other, in_taki: card.color == other.color,
    CardType.SUPER_TAKI: lambda card, other, in_taki: card.color == other.color
}


def valid_move(card, last_card=Card(None, '', ''), first=False, in_taki=False, plus_2_active=False):
    if first:
        return FIRST_STATE_MACHINE[last_card.type](last_card, card, plus_2_active)

    return REGULAR_STATE_MACHINE[last_card.type](last_card, card, in_taki)
