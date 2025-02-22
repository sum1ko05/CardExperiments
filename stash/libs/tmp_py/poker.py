from collections import Counter, OrderedDict
from cards import DynamicHand

class DynamicClassicPokerHand(DynamicHand):
    #This is Classic Poker hand, that inherits from DynamicHand
    #There would be calculations to see power of hand, comparing other hands, etc.
    def __init__(self):
        self._value_counter = Counter()
        self._hand_rank = [] #It would be used for comparing hands
        DynamicHand.__init__(self, enable_sorting=True)

    @property
    def hand_rank(self): #Getter
        self._update_stats
        return tuple(self._hand_rank) #I don't want to mutate this list separately from object

    #Overriding updating stats and sort function
    def _update_stats(self) -> None:
        self._value_counter = Counter([x.value for x in self._cards])
        self._sort()
        self._set_rank()
    
    def _sort(self) -> None:
        super()._sort(reversed=True)
        self._cards.sort(key=lambda c: self._value_counter[c.value], reverse=True)
    
    def _set_rank(self) -> None:
        self._hand_rank.clear()
        ranks = {'Incomplete': 0,
                 'High Card': 1,
                 'Pair': 2,
                 'Two Pairs': 3,
                 'Three of a Kind': 4,
                 'Wheel': 5,
                 'Straight': 6,
                 'Flush': 7,
                 'Full House': 8,
                 'Four of a Kind': 9,
                 'Steel wheel': 10,
                 'Straight Flush': 11}
        
        if len(self._cards) != 5: #Not valid hand
            self._hand_rank.append(ranks['Incomplete'])
            return #We need to prevent checking for rank while we don't have any cards
        
        bool_dict = OrderedDict() #Dict of booleans
        bool_dict['Straight Flush'] = self._is_straight_flush()
        bool_dict['Steel wheel'] = self._is_steel_wheel()
        bool_dict['Four of a Kind'] = self._is_four_of_a_kind()
        bool_dict['Full House'] = self._is_full_house()
        bool_dict['Flush'] = self._is_flush()
        bool_dict['Straight'] = self._is_straight()
        bool_dict['Wheel'] = self._is_wheel()
        bool_dict['Three of a Kind'] = self._is_three_of_a_kind()
        bool_dict['Two Pairs'] = self._is_two_pairs()
        bool_dict['Pair'] = self._is_pair()

        found_combo = False
        for k, fn in bool_dict.items(): #k - key, fn - value (did we find a combination?)
            if fn:
                self._hand_rank.append(ranks[k])
                found_combo = True
                break
        if not found_combo: 
            self._hand_rank.append(ranks['High Card'])
        self._hand_rank += [x.true_value for x in self._cards]
        pass

    def get_rank(self) -> list: #Only for debug purporse
        self._update_stats
        return self._hand_rank
    
    def __gt__(self, other):
        if self._hand_rank[0] == 0:
            return False #Comparing incomplete hands doesn't make any sense
        for i in range(min(len(self.hand_rank), len(other.hand_rank))):
            if self.hand_rank[i] != other.hand_rank[i]:
                return self.hand_rank[i] > other.hand_rank[i]
        return len(self.hand_rank) > len(other.hand_rank)
    
    def __lt__(self, other):
        if self._hand_rank[0] == 0:
            return False #Comparing incomplete hands doesn't make any sense
        for i in range(min(len(self.hand_rank), len(other.hand_rank))):
            if self.hand_rank[i] != other.hand_rank[i]:
                return self.hand_rank[i] < other.hand_rank[i]
        return len(self.hand_rank) < len(other.hand_rank)
    
    def __eq__(self, other):
        return self.hand_rank == other.hand_rank

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
        if [x.true_value for x in self._cards] == [14] + list(range(5, 1, -1)): #Ace-to-five => wheel
            return True #Found a wheel
        return False
    
    def _is_straight(self) -> bool:
        first_value = self._cards[0].true_value
        return [x.true_value for x in self._cards] == list(range(first_value, first_value - 5, -1))
    
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