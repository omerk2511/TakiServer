from card_type import CardType


class Card(object):
    def __init__(self, card_type, color, value):
        self.type = card_type
        self.color = color
        self.value = value

    def __eq__(self, other):
        if self.type == CardType.CHANGE_COLOR or \
                self.type == CardType.SUPER_TAKI:
            return self.type == other.type

        return (self.type == other.type and self.color == other.color and
                self.value == other.value)

    def serialize(self):
        return {
            'type': self.type,
            'color': self.color,
            'value': self.value
        }

    @classmethod
    def deserialize(cls, card):
        if 'type' not in card or 'color' not in card or 'value' not in card:
            raise Exception('Invalid card')

        return cls(card['type'], card['color'], card['value'])
