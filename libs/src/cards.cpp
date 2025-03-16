#include "../include/cards.hpp"
#include <iostream>
#include <cstdlib>

namespace playingcards
{
    void Card::swap(Card& other)
    {
        std::swap(m_value, other.m_value);
        std::swap(m_suit, other.m_suit);
    }

    Card::Card(Values value, Suits suit)
    {
        m_value = value;
        m_suit = suit;
    }

    //Only for assigning new values! Don't use it for literal copying!
    Card& Card::operator=(Card copy)
    {
        swap(copy);
        return *this;
    }

    Card::~Card()
    {

    }


}