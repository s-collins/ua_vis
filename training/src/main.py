import Tkinter as tk
import cv2 as cv
from controller import *
from models import TrainingExample
from views import *

class Parent:

    def __init__(self):
        self.root = tk.Tk()
        self.root.grid()

    def get_view(self):
        return self.root

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    image = cv.imread('image.jpg', cv.IMREAD_COLOR)
    training_example = TrainingExample(image)
    app = Parent()
    view = TrainingExampleEditorView(app.get_view())
    view.grid()
    labeler = LabelingEditorController(view.labeling_view, training_example)
    property_editor = PropertyEditorController(view.properties_view, training_example)
    app.run()

