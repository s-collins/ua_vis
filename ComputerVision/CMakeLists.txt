cmake_minimum_required(VERSION 3.0)
project(ComputerVision)

# third-party dependencies
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(NO_OUTPUT_DIRS)

# source code
add_subdirectory(src)

# unit tests
add_subdirectory(test)
