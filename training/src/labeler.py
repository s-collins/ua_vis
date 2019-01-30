import Tkinter as tk
import ttk
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
        self.sec_labeling = tk.LabelFrame(self, text='Labeling', padx=10, pady=10)
        self.lbl_image = tk.Label(self.sec_labeling)
        self.list = tk.Listbox(self.sec_labeling, height=5)
        self.but = tk.Button(self.sec_labeling, text='Remove Selected Label')

    def __layout_widgets(self):
        self.sec_labeling.grid(padx=10, pady=10)
        self.lbl_image.grid(row=0)
        self.list.grid(row=1, sticky='we')
        self.but.grid(row=2, sticky='we')

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
        self.labeling = False       # indicates whether or not currently labeling
        self.label_origin = None    # top-left coord of label in progress
        self.cross_pos = (0, 0)     # coord of center of cross
        self.view = LabelerView(self.parent.get_view())
        self.view.update_image(self.base_image)
        self.view.set_mouse_motion_callback(self.mouse_motion_callback)
        self.view.set_mouse_click_callback(self.mouse_click_callback)

    def mouse_motion_callback(self, event):
        """Updates the position of the cross and refreshes the image display."""
        self.cross_pos = (event.x, event.y)
        self.refresh_image_display()

    def refresh_image_display(self):
        """Updates the image in the GUI by drawing labels and cross to show mouse pos"""
        output = copy.deepcopy(self.base_image)
        self.draw_labels(output)
        self.draw_cross(output)
        if self.labeling:
            cv.rectangle(output, self.label_origin, self.cross_pos, self.BOX_COLOR, 1)
        self.view.update_image(output)

    def mouse_click_callback(self, event):
        """Responds to mouse click inside image by drawing a new label."""
        if self.labeling:
            new_label = (self.label_origin, (event.x, event.y))
            self.labels.append(new_label)
        else:
            self.label_origin = (event.x, event.y)
        self.labeling = not self.labeling
        self.refresh_image_display()

    def draw_labels(self, image):
        """Draws all of the existing labels on top of the given image."""
        for label in self.labels:
            cv.rectangle(image, label[0], label[1], self.BOX_COLOR, 2)

    def draw_cross(self, image):
        """Draws the cross on top of the given image."""
        height, width, channels = image.shape
        (x, y) = self.cross_pos
        line1 = ((0, y), (width, y))
        line2 = ((x, 0), (x, height))
        cv.line(image, line1[0], line1[1], self.CROSSHAIR_COLOR)
        cv.line(image, line2[0], line2[1], self.CROSSHAIR_COLOR)


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
