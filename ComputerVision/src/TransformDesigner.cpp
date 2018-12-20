#include "ComputerVision/TransformDesigner.hpp"
#include "ComputerVision/Image.hpp"
#include "ComputerVision/Parameter.hpp"
#include "ComputerVision/Transform.hpp"
#include <iostream>

namespace ComputerVision {

  void
  TransformDesigner::run (Image & image,
                          std::shared_ptr<Transform> transform)
  {
    // display original image in its own window
    cv::imshow("Original", image);

    // set parameter values (by getting input)
    // TODO: 'getParams' should return a map (string, param) so
    //       that it is easy to hard-code parameter values if
    //       necessary.
    populateParams(transform->getParams());

    // apply the transformation
    transform->applyTo(image);

    // display result in its own window
    cv::imshow("After Transform", image);

    // wait for ESC keypress
    std::cout << "Press <ESC> to close windows and exit.\n";
    if (cv::waitKey() == 27)
      cv::destroyAllWindows();
  }

  void
  TransformDesigner::populateParams
  (std::vector<std::shared_ptr<Parameter>> const & params)
  {
    for (auto const & param : params)
      std::cout << param->getName() << '\n';
  }

} // namespace ComputerVision
