#pragma once
#include "opencv2/opencv.hpp"

namespace ComputerVision {

  class Image : public cv::Mat
  {
  public:
  	Image(const cv::Mat& mat)
  	:Mat(mat)
  	{}
  };

} // namespace ComputerVision
