HAND_INITIAL_SIZE = 8


class Hand(object):
    def __init__(self, cards):
        self.cards = cards

    def append_cards(self, cards):
        self.cards.extend(cards)
