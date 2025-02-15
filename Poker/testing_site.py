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

#Passing needed tests here
if __name__=="__main__":
    pass_test1_deck()
