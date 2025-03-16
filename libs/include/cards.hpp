#pragma once
#include <iostream>
#include <cstdlib>

namespace playingcards
{
    //We can use finite states here at least (we can refactor this later lmao)
    enum class Values {D2 = 2, D3, D4, D5, D6, D7, D8, D9, D10, Jack, Queen, King, Ace};
    enum class Suits {Hearts, Clubs, Diamonds, Spades};

    //Your default playing card
    class Card
    {
    private:
        Values m_value;
        Suits m_suit;

        void swap(Card& other);
    public:
        Card(Values value, Suits suit);
        Card& operator=(Card copy);
        ~Card();

        //IO streams (no istream)
        friend std::ostream& operator<<(std::ostream& out, const Card& card)
        {
            //Picking symbols for values
            switch(card.m_value)
            {
                case Values::Jack: out << "J"; break;
                case Values::Queen: out << "Q"; break;
                case Values::King: out << "K"; break;
                case Values::Ace: out << "A"; break;
                default: out << std::to_string((int)card.m_value); break;
            }
            //Picking symbold for suits
            switch(card.m_suit)
            {
                case Suits::Hearts: out << "♥"; break;
                case Suits::Clubs: out << "♣"; break;
                case Suits::Diamonds: out << "♦"; break;
                case Suits::Spades: out << "♠"; break;
            }
            return out;
        }
    };
}
