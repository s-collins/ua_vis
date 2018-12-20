#include "ComputerVision/Parameter.hpp"
#include <stdexcept>

namespace ComputerVision {

  /*------------------------------ Constructors ------------------------------*/

  Parameter::Parameter (std::string name,
                        int def,
                        int minimum,
                        int maximum)
    : name_(std::move(name)),
      type_(INTEGER)
  {
    value_.whole_num = def;
    min_.whole_num = minimum;
    max_.whole_num = maximum;
  }

  Parameter::Parameter (std::string name,
                        double def,
                        double minimum,
                        double maximum)
    : name_(std::move(name)),
      type_(DOUBLE)
  {
    value_.real_num = def;
    min_.real_num = minimum;
    max_.real_num = maximum;
  }

  /*-------------------------------- Mutators --------------------------------*/
  
  void
  Parameter::setValue (int value)
  {
    if (type_ != INTEGER)
      throw std::logic_error {"Error: Mismatched type in param assignment."};
    if ((value < min_.whole_num) || (value > max_.whole_num))
      throw std::logic_error {"Error: Setting param to out of range value."};
    value_.whole_num = value;
  }

  void
  Parameter::setValue (double value)
  {
    if (type_ != DOUBLE)
      throw std::logic_error {"Error: Mismatched type in param assignment."};
    if ((value < min_.real_num) || (value > max_.real_num))
      throw std::logic_error {"Error: Setting param to out of range value."};
    value_.real_num = value;
  }

  /*-------------------------------- Accessors -------------------------------*/

  int
  Parameter::getIntegerValue () const
  {
    if (type_ != INTEGER)
      throw std::logic_error {"Error: Read integer from non-integer param."};
    return value_.whole_num;
  }

  double
  Parameter::getDoubleValue () const
  {
    if (type_ != DOUBLE)
      throw std::logic_error {"Error: Read double from non-double param."};
    return value_.real_num;
  }

  Parameter::Type
  Parameter::getType () const
  {
    return type_;
  }

  std::string const &
  Parameter::getName () const
  {
    return name_;
  }

} // namespace ComputerVision
