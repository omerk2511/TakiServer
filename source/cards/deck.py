import random
from card import Card
from card_type import CardType
from hand import Hand, HAND_INITIAL_SIZE

COLORS = ['red', 'blue', 'green', 'yellow']
NUMBERS = [1, 3, 4, 5, 6, 7, 8, 9]


def build_color_cards(color):
    return ([Card(CardType.NUMBER_CARD, color, number) for number in NUMBERS] +
            [Card(CardType.STOP, color, ''), Card(CardType.PLUS, color, ''),
             Card(CardType.TAKI, color, ''),
             Card(CardType.CHANGE_DIRECTION, color, '')])


def build_initial_deck():
    return (reduce(lambda x, y: x + y,
                   [build_color_cards(color) for color in COLORS]) +
            [Card(CardType.CHANGE_COLOR, '', '')] * 2 +
            [Card(CardType.SUPER_TAKI, '', '')] * 2) * 2


class Deck(object):
    def __init__(self):
        self.cards = build_initial_deck()
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def get_random_card(self):
        return self.cards.pop()

    def get_random_cards(self, amount=1):
        return [self.cards.pop() for _ in xrange(amount)]

    def get_hand(self):
        return Hand([self.cards.pop() for _ in xrange(HAND_INITIAL_SIZE)])

    def add_card(self, card):
        self.cards.insert(0, card)
