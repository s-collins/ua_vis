#pragma once
#include "opencv2/opencv.hpp"
#include <string>
#include "Image.hpp"

namespace ComputerVision{

	//possible base class for UI components

	class Component{
	public:
		enum Type{
			WINDOW,
			TRACKBAR
		};
	private:
		Type type_;

	public:
		Component(Type type)
		:type_(type)
		{} 

		Type getType() const {return type_;}

		virtual void create() = 0;
	};


	//Possible wrapper class
	//Wraps the window functions from opencv 
	//allows a single window to be tracked by it's name
	//makes manipulation of a single window easier to track 
	//Allows windows to appear as objects
	class Window : public Component{
	private:
		std::string name_;

		//creates widnow using the namedWindow function
		void create() override;

	public:
		//constuctors

		//TODO: default constructor will have a window with the empty string as the name
		//		However multiple objects created with the default constructor
		//		will not create another window


		//creates window with specified name 
		Window(std::string name);

		//displays image object using imshow function 
		Window(std::string name, Image& image);

		//resizes window with specified dimensions
		void resize(int width, int height);

	};
};

