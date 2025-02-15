from collections import Counter, OrderedDict
import random
import secrets

#List of strings to generate cards
#H - hearts, C - clubs, D - diamonds, S - spades
STRING_DECK = ['%s%s' % (value, suit) for suit in 'HCDS' for value in list(['A'] + list(range(2,11)) + ['J', 'Q', 'K'])]

class Card: 
    def __init__(self, c: str): #String format: [characters of value][character of suit]
        self.__value = c[:-1] #excluding last character
        self.__suit = c[-1] #including only last character
        self.__set_true_value()
        self.__id = secrets.token_hex(16) #Assigning token hex for future sanity check

    #Calculating for easier value comparing
    def __set_true_value(self) -> None:
        elders = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        self.__true_value = 0
        try:
            self.__true_value = int(self.__value)
        except ValueError: #Not a number - probably elder card
            self.__true_value = elders[self.__value]

    #You shouldn't change anything in cards, so any values of cards are read-only
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
    
    #It'll return stuff that will show you when you pass this object to print() or str()
    def __str__(self):
        return str(str(self.value) + str(self.suit))
    
class DynamicHand:
    #There are only basic properties of any card hand
    #If you want more possibilities, you have to create inherited class
    def __init__(self, cards: list | None = None, enable_sorting: bool = False):
        if cards == None:
            self._cards = []
        else:
            self._cards = cards
        self._enable_sorting = enable_sorting
        self._update_stats()

    #Just inserting card into hand (mosly from deck)
    #You need to pass there Card object since i want to prevent cheating
    #Calculations with cards are planned in inherited classes
    def append(self, card: Card) -> None:
        self._cards.append(card)
        self._update_stats()

    #Internal function for seeking card by string value
    def _find_card_by_str(self, c: str) -> Card | None:
        target_card = Card(c)
        for card in self._cards:
            if target_card.true_value == card.true_value:
                if target_card.suit == card.suit:
                    return card
        return None

    #Just drawing card from hand
    #You can pass both str and Card objects since calling function is basically a request
    def draw(self, card: str|Card) -> Card | None:
        if type(card) == str:
            drawn_card = self._find_card_by_str(c=card)
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

    #Function that should be called after any change in hand
    #Could be overriden in inherited classes, because stats are diffrent for any game
    def _update_stats(self) -> None:
        if self._enable_sorting:
            self._sort(priority="values")
        pass

    #Stable sorting cards with variable priority
    #For example, in poker suits doesn't matter unless you have mono-suit hand
    #But in Durak (traditional Russian card game) suits matter, so you would want to sort by suits first
    def _sort(self, priority: str = "values") -> None:
        if priority not in ["values", "suits"]:
            raise ValueError
        if priority == "suits":
            self._cards.sort(key=Card.suit)
            self._cards.sort(key=Card.true_value)
        if priority == "values":
            self._cards.sort(key=Card.true_value)
            self._cards.sort(key=Card.suit)
        pass
    
    #It'll return stuff that will show you when you pass this object to print() or str()
    def __str__(self):
        string = ""
        for c in self._cards:
            string += str(c.value) + str(c.suit) + " "
        return string

class DynamicClassicPokerHand(DynamicHand):
    #This is Classic Poker hand, that inherits from DynamicHand
    #There would be calculations to see power of hand, comparing other hands, etc.
    def __init__(self):
        DynamicHand.__init__(self, enable_sorting=True)
        self._value_counter = Counter()
        self._hand_rank = [] #It would be used for comparing hands

    #Overriding updating stats
    def _update_stats(self) -> None:
        self._sort(priority="values")
        self._value_counter = Counter([x.value for x in self._cards])

    def _set_rank(self) -> None:
        pass

    #Reminder for Counter
    #We have dict inside, so for amounts of cards we have to check values of that dict

    #Checking for combinations
    def _is_pair(self) -> bool: 
        return max(self._value_counter.values()) == 2 
    
    def _is_two_pairs(self) -> bool:
        return list(self._value_counter.values()).count(2) == 2 #Two times two cards with same value
    
    def _is_three_of_a_kind(self) -> bool:
        return max(self._value_counter.values()) == 3

    #We should sort hand first before checking for any combos
    def _is_wheel(self) -> bool: #Kind of straight, calculating it separately for easier comparing
        if [x.true_value for x in self._cards] == list(range(2, 6)) + [14]: #Ace-to-five => wheel
            return True #Found a wheel
        return False
    
    def _is_straight(self) -> bool:
        first_value = self._cards[0].true_value
        return [x.true_value for x in self._cards] == list(range(first_value, first_value + 5))
    
    def _is_flush(self) -> bool:
        return len(set([x.suit for x in self._cards])) == 1
    
    def _is_full_house(self) -> bool:
        return 3 in self._value_counter.values() and 2 in self._value_counter.values()
    
    def _is_four_of_a_kind(self) -> bool:
        return max(self._value_counter.values()) == 4
    
    def _is_steel_wheel(self) -> bool:
        return self._is_wheel() and self._is_flush()
    
    def _is_straight_flush(self) -> bool:
        return self._is_straight() and self._is_flush()
    #We don't differentiate royal flush since it easily calculates through straight flush

class Deck(DynamicHand):
    #Just creating deck and shuffling it
    #Any operations with DynamicHand are also working with Deck
    def __init__(self):
        super().__init__()
        for c in STRING_DECK:
            while True:
                new_card = Card(c)
                if new_card.id not in [x.id for x in self._cards]:
                    self._cards.append(new_card)
                    break
        random.shuffle(self._cards)

    #You can draw only from top of deck, so you don't have to specify card that you want to draw
    def draw(self) -> Card | None:
        if len(self._cards) > 0:
            return super().draw(self._cards[0])
        return None