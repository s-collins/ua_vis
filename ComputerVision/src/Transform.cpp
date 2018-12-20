#include "ComputerVision/Transform.hpp"

namespace ComputerVision {

  void
  MultiTransform::add (std::shared_ptr<Transform> child)
  {
    children_.push_back(child);
  }

  void
  MultiTransform::applyTo (Image & image) const
  {
    for (auto const & transformation : children_)
      transformation->applyTo(image);
  }

  PtrList<Parameter> const
  MultiTransform::getParams ()
  {
    PtrList<Parameter> params;
    for (auto & child : children_)
      for (auto & param : child->getParams())
        params.push_back(param);
    return params;
  }

} // namespace ComputerVision
