class Card(object):
    def __init__(self, card_type, color, value):
        self.type = card_type
        self.color = color
        self.value = value

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
