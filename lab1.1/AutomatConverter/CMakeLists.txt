cmake_minimum_required (VERSION 3.8)

project (AutomatConverter)

set(CMAKE_CXX_STANDARD 20)

add_executable (AutomatConverter AutomatConverter.cpp AutomatConverter.h "CMealy.h" "CMealy.cpp" "CMoore.cpp" "CMoore.h" "utils.cpp" "utils.h")
