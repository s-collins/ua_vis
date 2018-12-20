#pragma once
#include <memory>
#include <vector>
#include "opencv2/opencv.hpp"

namespace ComputerVision {

  class Image;
  class Parameter;
  class Transform;

  class TransformDesigner {
  public:
    void run (Image &, std::shared_ptr<Transform>);
    /// Run the transform designer application.
    
  private:
    void populateParams (std::vector<std::shared_ptr<Parameter>> const &);
    /// Runs a UI to obtain values for a set of parameters.
  };

} // namespace ComputerVision
