from collections import defaultdict


class Cards(object):

    def __init__(self):
        self.cards = defaultdict(list)

    def add(self, room_id, card):
        self.cards[room_id].append(card)

    def get_all(self, room_id):
        return self.cards[room_id]

    def update_xy(self, room_id, card_id, x, y):
        i = self.index(room_id, card_id)
        if i != -1:
            self.cards[room_id][i]['x'] = x
            self.cards[room_id][i]['y'] = y

    def update_text(self, room_id, card_id, text):
        i = self.index(room_id, card_id)
        if i != -1:
            self.cards[room_id][i]['text'] = text

    def delete(self, room_id, card_id):
        i = self.index(room_id, card_id)
        if i != -1:
            del self.cards[room_id][i]

    def index(self, room_id, card_id):
        for i, card in enumerate(self.cards[room_id]):
            if card['id'] == card_id:
                return i
        return -1