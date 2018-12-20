#pragma once
#include <limits>
#include <string>

namespace ComputerVision {

  /*--------------------------------- Helpers --------------------------------*/
  
  template <typename T>
  constexpr T minValue ()
  {
    return std::numeric_limits<T>::min();
  }
 
  template <typename T>
  constexpr T maxValue ()
  {
    return std::numeric_limits<T>::max();
  }

  /*----------------------------- Parameter Class ----------------------------*/

  class Parameter {
  public:
    enum Type {
      INTEGER,
      DOUBLE
    };

  public:
    // CONSTRUCTORS
    Parameter (std::string name,
               int def = minValue<int>(),
               int = minValue<int>(),
               int = maxValue<int>());
    Parameter (std::string name,
               double def = minValue<double>(),
               double = minValue<double>(),
               double = maxValue<double>());

    // MUTATORS
    void setValue (int);
    void setValue (double);

    // ACCESSORS
    int getIntegerValue () const;
    double getDoubleValue () const;
    Type getType () const;

  private:
    union Representation {
      int whole_num;
      double real_num;
    };

    std::string name_;
    Type type_;
    Representation value_;
    Representation min_;
    Representation max_;
  };

} // namespace ComputerVision
