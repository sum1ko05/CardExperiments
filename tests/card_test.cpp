#include <iostream>
#include "../libs/include/cards.hpp"

int main()
{
    playingcards::Card c = playingcards::Card(playingcards::Values::Jack, 
                                              playingcards::Suits::Hearts);
    std::cout << c << std::endl;
    return 0;
}