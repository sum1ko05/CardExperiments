from collections import Counter, OrderedDict
import random
import secrets

#H - hearts, C - clubs, D - diamonds, S - spades
STRING_DECK = ['%s%s' % (value, suit) for suit in 'HCDS' for value in list(['A'] + list(range(2,11)) + ['J', 'Q', 'K'])]

class Card: 
    def __init__(self, c: str): #String format: [characters of value][character of suit]
        self.__value = c[:-1] #excluding last character
        self.__suit = c[-1] #including only last character
        self.__set_true_value()
        self.__id = secrets.token_hex(16) #Assigning token hex for future sanity check

    def __set_true_value(self):
        elders = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        self.__true_value = 0
        try:
            self.__true_value = int(self.__value)
        except ValueError: #Not a number - probably elder card
            self.__true_value = elders[self.__value]

    @property
    def value(self): #Getter
        return self.__value
    
    @property
    def true_value(self): #Getter
        return self.__true_value
    
    @property
    def suit(self): #Getter
        return self.__suit
    
    @property
    def id(self): #Getter
        return self.__id
    
    def __str__(self):
        return str(str(self.value) + str(self.suit))

def list_str_to_card(strings: list):
    pass
    
class DynamicHand:
    def __init__(self, cards: list | None = None, enable_sorting: bool = False):
        if cards == None:
            self._cards = []
        else:
            self._cards = cards
        self._enable_sorting = enable_sorting
        self._update_stats()

    def append(self, card: Card):
        self._cards.append(card)
        self._update_stats()

    def find_card_by_str(self, c: str):
        target_card = Card(c)
        for card in self._cards:
            if target_card.true_value == card.true_value:
                if target_card.suit == card.suit:
                    return card
        return None

    def draw(self, card: str|Card):
        if type(card) == str:
            drawn_card = self.find_card_by_str(c=card)
            try:
                self._cards.remove(drawn_card)
            except ValueError:
                return None #Card not found
            self._update_stats()
            return drawn_card
        elif type(card) == Card:
            drawn_card = card
            try:
                self._cards.remove(drawn_card)
            except ValueError:
                raise ValueError #We can except this external error later
            self._update_stats()
            return drawn_card

    def _update_stats(self):
        if self._enable_sorting:
            self._sort(priority="values")
        pass

    def _sort(self, priority: str):
        if priority not in ["values", "suits"]:
            raise ValueError
        if priority == "suits":
            self._cards.sort(key=Card.suit)
            self._cards.sort(key=Card.true_value)
        if priority == "values":
            self._cards.sort(key=Card.true_value)
            self._cards.sort(key=Card.suit)
        pass

    def __str__(self):
        string = ""
        for c in self._cards:
            string += str(c.value) + str(c.suit) + " "
        return string

class DynamicClassicPokerHand(DynamicHand):
    def __init__(self):
        DynamicHand.__init__(self, enable_sorting=True)

    def _update_stats(self):
        self._sort(priority="values")

class Deck(DynamicHand):
    def __init__(self):
        super().__init__()
        for c in STRING_DECK:
            while True:
                new_card = Card(c)
                if new_card.id not in [x.id for x in self._cards]:
                    self._cards.append(new_card)
                    break
        random.shuffle(self._cards)

    def draw(self):
        if len(self._cards) > 0:
            return super().draw(self._cards[0])
        return None

deck = Deck()
print(deck)
hand = DynamicHand()
for i in range(0, 5):
    hand.append(deck.draw())
print(hand)
print(deck)
#print(STRING_DECK)