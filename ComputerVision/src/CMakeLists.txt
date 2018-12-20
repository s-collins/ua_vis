add_library(ComputerVision
  Transform.cpp
  Parameter.cpp
)
target_include_directories(ComputerVision PUBLIC include)
target_link_libraries(ComputerVision
  PRIVATE
    ${CONAN_LIBS}
)
