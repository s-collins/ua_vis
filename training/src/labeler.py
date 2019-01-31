import Tkinter as tk
import ttk
from PIL import Image
from PIL import ImageTk
import cv2 as cv
import copy


class TrainingExample:

    def __init__(self, image, labels=None):
        self.image = image
        self.labels = labels
        if self.labels is None:
            self.labels = []


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

    def set_list_selection_callback(self, callback):
        self.list.bind('<<ListboxSelect>>', callback)

    def set_delete_selected_command(self, callback):
        self.but.config(command=callback)

    def refresh_image(self, cv_image):
        im = cv.cvtColor(cv_image, cv.COLOR_BGR2RGB)
        im = Image.fromarray(im)
        im = ImageTk.PhotoImage(im)
        self.lbl_image.configure(image=im)
        self.lbl_image.image = im

    def refresh_label_list(self, labels, selected):
        self.list.delete(0, tk.END)
        for label in labels:
            text = str(label[0]) + ', ' + str(label[1])
            self.list.insert(tk.END, text)
        if selected is not None:
            self.list.selection_set(selected)


class LabelerPresentationModel:

    # uses (blue, green, red) format
    CROSS_COLOR = (0, 0, 255)
    BOX_COLOR = (0, 255, 0)
    SELECTED_BOX_COLOR = (255, 0, 0)
    BOX_IN_PROGRESS_WEIGHT = 1
    BOX_FINISHED_WEIGHT = 2

    def __init__(self, parent, training_example):
        self.parent = parent
        self.training_example = training_example
        self.labeling = False
        self.box = [None, None]
        self.cross = (0, 0)
        self.selected_label = None
        self.view = LabelerView(self.parent.get_view())
        self.view.set_mouse_motion_callback(self.mouse_motion_callback)
        self.view.set_mouse_click_callback(self.mouse_click_callback)
        self.view.set_list_selection_callback(self.list_selection_callback)
        self.view.set_delete_selected_command(self.delete_selected)
        self.refresh_image()
        self.refresh_label_list()

    def refresh_image(self):
        """Updates the image in the GUI by drawing labels and cross."""
        output = copy.deepcopy(self.training_example.image)
        self.draw_labels(output)
        self.draw_cross(output)
        self.draw_box(output)
        self.view.refresh_image(output)

    def refresh_label_list(self):
        """Updates the GUI's listbox so that it contains coordinates of current labels."""
        self.view.refresh_label_list(self.training_example.labels, self.selected_label)

    def draw_labels(self, image):
        """Draws all of the existing labels on top of the given image."""
        for i in range(len(self.training_example.labels)):
            label = self.training_example.labels[i]
            if i == self.selected_label:
                cv.rectangle(image, label[0], label[1], self.SELECTED_BOX_COLOR, 2)
            else:
                cv.rectangle(image, label[0], label[1], self.BOX_COLOR, 2)

    def draw_cross(self, image):
        """Draws the cross on top of the given image."""
        height, width, channels = image.shape
        (x, y) = self.cross
        line1 = ((0, y), (width, y))
        line2 = ((x, 0), (x, height))
        cv.line(image, line1[0], line1[1], self.CROSS_COLOR)
        cv.line(image, line2[0], line2[1], self.CROSS_COLOR)

    def draw_box(self, image):
        if self.labeling:
            cv.rectangle(image, self.box[0], self.box[1], self.BOX_COLOR, self.BOX_IN_PROGRESS_WEIGHT)

    def mouse_motion_callback(self, event):
        """Updates the position of the cross and refreshes the image display."""
        self.cross = (event.x, event.y)
        self.box[1] = self.cross
        self.refresh_image()

    def mouse_click_callback(self, event):
        """Responds to mouse click inside image by drawing a new label."""
        if self.labeling:
            self.box[1] = (event.x, event.y)
            self.training_example.labels.append(self.box)
            self.selected_label = len(training_example.labels) - 1
            self.box = [None, None]
        else:
            self.box[0] = (event.x, event.y)
        self.refresh_label_list()
        self.refresh_image()
        self.labeling = not self.labeling

    def list_selection_callback(self, event):
        """Updates the selected label."""
        self.selected_label = event.widget.curselection()[0]
        self.refresh_image()

    def delete_selected(self):
        """Removes currently selected label."""
        if self.selected_label is None:
            return
        labels = self.training_example.labels
        if self.selected_label < len(labels):
            del labels[self.selected_label]
        self.refresh_label_list()
        self.refresh_image()


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
training_example = TrainingExample(image)
labeler = LabelerPresentationModel(app, training_example)
app.run()




