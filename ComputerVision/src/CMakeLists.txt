add_library(ComputerVision
  Parameter.cpp
  Transform.cpp
  TransformDesigner.cpp
  Window.cpp
)
target_include_directories(ComputerVision PUBLIC include)
target_link_libraries(ComputerVision
  PRIVATE
    ${CONAN_LIBS}
)
