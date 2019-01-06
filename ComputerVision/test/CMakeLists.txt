cmake_minimum_required(VERSION 3.0)
project(ComputerVisionTests)

# test dependencies
enable_testing()
find_package(GTest REQUIRED)

# test executable
add_executable(ComputerVisionTests 
				ComputerVisionTests.cpp
				ComponentTests.cpp)
target_link_libraries(ComputerVisionTests
  PRIVATE
    ComputerVision
    GTest::Main
)
