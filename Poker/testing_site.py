import cards_lib as cl
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

def pass_test1_poker_hand(): #Testing checking for combination
    test_string = ["6D", "7D", "8D", "6C", "7H"]
    test_hand = cl.DynamicClassicPokerHand()
    for c in test_string:
        new_card = cl.Card(c)
        test_hand.append(new_card)
    print(test_hand)
    print(test_hand.get_rank())

#Passing needed tests here
if __name__=="__main__":
    pass_test1_poker_hand()
