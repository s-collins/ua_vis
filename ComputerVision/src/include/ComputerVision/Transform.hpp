#pragma once
#include <memory>
#include <vector>
class Image;
class Parameter;

// TODO: Consider whether it would be better for parameters to
//       be returned as unordered maps.  This would allow me to
//       easily associate a name with each parameter.

// TODO: Consider whether or not it is necessary to store parameters
//       in shared pointers.  I do not think they will be allocated
//       on the heap, so it may be better for 'getParams' to return
//       a vector by reference.

namespace ComputerVision {

  /*--------------------------------- Helpers --------------------------------*/

  template <typename T>
  using PtrList = std::vector<std::shared_ptr<T>>;
  /// Alias for a list of shared pointers.
  
  /*----------------------------- Transform Class ----------------------------*/

  class Transform {
  public:
    virtual void applyTo (Image &) const = 0;
    /// Applies the transformation to the image.
    
    virtual PtrList<Parameter> const getParams () = 0;
    /// Returns a list of parameters that can be adjusted to configure
    /// the transformation.
  };

  /*-------------------------- MultiTransform Class --------------------------*/

  class MultiTransform : public Transform {
  public:
    virtual void add (std::shared_ptr<Transform> child);
    /// Add a child transformation.

    void applyTo (Image & image) const override;
    /// Apply all transformations in the tree by using a post-order traversal.
    
    PtrList<Parameter> const getParams () override;
    /// Returns a list of parameters that can be adjusted to configure
    /// the transformation. Parameters are listed in order of post-order
    /// traversal.
    
  private:
    PtrList<Transform> children_;
  };

} // namespace ComputerVision
