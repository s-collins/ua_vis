#include "gtest/gtest.h"
#include "ComputerVision/Component.hpp"


TEST(ComponentTest,Windows){

	ComputerVision::Image image = static_cast<ComputerVision::Image>(cv::imread("wallpaper.jpg"));
	ComputerVision::Window window("Test Window",image);

	// EXPECT_EQ(window.getType(),ComputerVision::Component::WINDOW);
}

int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}