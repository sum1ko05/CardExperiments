cmake_minimum_required(VERSION 3.8)

project(cpp_card_project
    VERSION 0.3
    LANGUAGES CXX)

set_target_properties(${TARGET} PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED YES
    CXX_EXTENSIONS NO
)

# Setting source files for building
set(SOURCES
    tests/card_test.cpp
    libs/src/cards.cpp)

# Adds executable with sources listed above
add_executable(CardTest ${SOURCES})

# Set the directories that should be included in the build command for this target
# <target> from here should be same as <name> from add_executable earlier
target_include_directories(CardTest
    PRIVATE ${PROJECT_SOURCE_DIR}/libs/include
)