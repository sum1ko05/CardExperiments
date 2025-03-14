#pragma once
#include <iostream>
#include <cstdlib>

namespace cards
{
    enum class Values {D2 = 2, D3, D4, D5, D6, D7, D8, D9, D10, Jack, Queen, King, Ace};
    enum class Suits {Hearts, Clubs, Diamonds, Spades};

    //Your default playing card
    class Card
    {
    private:
        Values m_value;
        Suits m_suit;

        void swap(Card& other)
        {
            std::swap(m_value, other.m_value);
            std::swap(m_suit, other.m_suit);
        }
    public:
        Card(Values value, Suits suit)
        {
            m_value = value;
            m_suit = suit;
        }
        //Only for assigning new values! Don't use it for copying!
        Card& operator=(Card copy)
        {
            swap(copy);
            return *this;
        }
        ~Card()
        {
            
        };

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
