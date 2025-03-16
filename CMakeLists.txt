cmake_minimum_required(VERSION 3.8)

project(cpp_card_project
    VERSION 0.3
    LANGUAGES CXX)

set_target_properties(${TARGET} PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED YES
    CXX_EXTENSIONS NO
)

add_executable(CardTest 
    tests/card_test.cpp
    libs/include/cards/cards.hpp
)