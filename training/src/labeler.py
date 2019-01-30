"""
Types of Events:

 - Mouse motion over the image
 - Click event on the image
"""

import Tkinter as tk
from PIL import Image
from PIL import ImageTk
import cv2 as cv
import copy


class LabelerView(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.grid()

        # Configure the view
        self.__create_widgets()
        self.__layout_widgets()

    def __create_widgets(self):
        self.lbl_image = tk.Label(self)

    def __layout_widgets(self):
        self.lbl_image.grid()

    def set_mouse_motion_callback(self, callback):
        self.lbl_image.bind('<Motion>', callback)

    def set_mouse_click_callback(self, callback):
        self.lbl_image.bind('<Button-1>', callback)

    def update_image(self, cv_image):
        im = cv.cvtColor(cv_image, cv.COLOR_BGR2RGB)
        im = Image.fromarray(im)
        im = ImageTk.PhotoImage(im)
        self.lbl_image.configure(image=im)
        self.lbl_image.image = im


class LabelerPresentationModel:

    # uses (blue, green, red) format
    CROSSHAIR_COLOR = (0, 0, 255)
    BOX_COLOR = (0, 255, 0)

    def __init__(self, parent, cv_image):
        self.parent = parent
        self.base_image = cv_image
        self.labels = []

        # indicates whether or not currently labeling
        self.labeling = False
        self.label_origin = None

        # Initialize the view
        self.view = LabelerView(self.parent.get_view())
        self.view.update_image(self.base_image)
        self.view.set_mouse_motion_callback(self.mouse_motion_callback)
        self.view.set_mouse_click_callback(self.mouse_click_callback)

    def mouse_motion_callback(self, event):
        """Updates the position of the crosshair and refreshes the image display."""
        image = copy.deepcopy(self.base_image)
        self.draw_labels(image)
        self.draw_crosshair(image, event.x, event.y)
        if self.labeling:
            cv.rectangle(image, self.label_origin, (event.x, event.y), LabelerPresentationModel.BOX_COLOR, 1)
        self.view.update_image(image)

    def mouse_click_callback(self, event):
        if self.labeling:
            new_label = (self.label_origin, (event.x, event.y))
            self.labels.append(new_label)
            self.labeling = False
        else:
            self.label_origin = (event.x, event.y)
            self.labeling = True
#
    def draw_labels(self, image):
        for label in self.labels:
            cv.rectangle(image, label[0], label[1], LabelerPresentationModel.BOX_COLOR, 2)

    def draw_crosshair(self, image, x, y):
        height, width, channels = image.shape
        line1 = ((0, y), (width, y))
        line2 = ((x, 0), (x, height))
        cv.line(image, line1[0], line1[1], LabelerPresentationModel.CROSSHAIR_COLOR)
        cv.line(image, line2[0], line2[1], LabelerPresentationModel.CROSSHAIR_COLOR)

class Parent:

    def __init__(self):
        self.root = tk.Tk()
        self.root.grid()

    def get_view(self):
        return self.root

    def run(self):
        self.root.mainloop()


app = Parent()
image = cv.imread('image.jpg', cv.IMREAD_COLOR)
labeler = LabelerPresentationModel(app, image)
app.run()
