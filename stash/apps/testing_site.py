import libs.base.cards as cl
from libs.poker.poker import DynamicClassicPokerHand
#This part of code now is mosly used for testing
#This file would be removed since it's not nessesary to keep it in repo

def pass_test1_deck(): #Testing drawing from deck
    deck = cl.Deck()
    print(deck)
    hand = cl.DynamicHand()
    for i in range(0, 5):
        hand.append(deck.draw())
    print(hand)
    print(deck)

def pass_test2_poker_hand(): #Testing checking for combination
    test_string = ["3D", "3C", "3H", "9D", "9H"]
    test_hand = DynamicClassicPokerHand()
    for c in test_string:
        new_card = cl.Card(c)
        test_hand.append(new_card)
    print(test_hand)
    print(test_hand.hand_rank)

def pass_test3_poker_hand_comparing(): #Testing comparing hands and looking for a winner
    #Test for 4 people
    deck = cl.Deck()
    test_table = [DynamicClassicPokerHand(),
                  DynamicClassicPokerHand(),
                  DynamicClassicPokerHand(),
                  DynamicClassicPokerHand()]
    for i in range(0, 5):
        for hand in test_table:
            hand.append(deck.draw())
    for hand in test_table:
        print(hand)
    print("Winner: ", end="")
    print(max(test_table))

#Passing needed tests here
if __name__=="__main__":
    pass_test3_poker_hand_comparing()
