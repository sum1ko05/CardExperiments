#include <iostream>
#include "../libs/cards/cards.hpp"

int main()
{
    cards::Card c = cards::Card(cards::Values::D10, 
                                cards::Suits::Hearts);
    std::cout << c << std::endl;
    return 0;
}