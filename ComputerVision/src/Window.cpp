#include "ComputerVision/Component.hpp"


namespace ComputerVision{

	/*------------------------------ Constructors ------------------------------*/
	Window::Window(std::string name)
	:Component(WINDOW), name_(name)	
	{
		create();
	}

	Window::Window(std::string name, Image& image)
	:Component(WINDOW),name_(name)	
	{
		cv::imshow(name_,image);
	}

	/*------------------------------ Modifiers ------------------------------*/
	void Window::resize(int width, int height)
	{
		cv::resizeWindow(name_,width,height);
	}

	/*------------------------------ Initializer ------------------------------*/
	void Window::create() 
	{
		cv::namedWindow(name_);
	}
};

