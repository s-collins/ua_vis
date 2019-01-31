import cv2 as cv
import copy
from models import *


class LabelingEditorController:

    # uses (blue, green, red) format
    CROSS_COLOR = (0, 0, 255)
    BOX_COLOR = (0, 255, 0)
    SELECTED_BOX_COLOR = (255, 0, 0)
    BOX_IN_PROGRESS_WEIGHT = 1
    BOX_FINISHED_WEIGHT = 2

    ####################################################################################################################
    # INITIALIZATION
    ####################################################################################################################

    def __init__(self, view, training_example):
        self.training_example = training_example
        self.labeling = False
        self.box = [None, None]
        self.cross = (0, 0)
        self.selected_label = None
        self.view = view
        self.__assign_callbacks()
        self.refresh_view()

    def __assign_callbacks(self):
        self.view.set_mouse_motion_callback(self.mouse_motion_callback)
        self.view.set_mouse_click_callback(self.mouse_click_callback)
        self.view.set_list_selection_callback(self.list_selection_callback)
        self.view.set_delete_selected_command(self.delete_selected)

    ####################################################################################################################
    # REFRESHING THE VIEW
    ####################################################################################################################

    def refresh_view(self):
        self.refresh_label_list()
        self.refresh_image()

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

    ####################################################################################################################
    # SHAPE DRAWING
    ####################################################################################################################

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

    ####################################################################################################################
    # CALLBACKS
    ####################################################################################################################

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
            self.selected_label = len(self.training_example.labels) - 1
            self.box = [None, None]
        else:
            self.box[0] = (event.x, event.y)
        self.refresh_view()
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
        self.refresh_view()


class PropertyEditorController:

    def __init__(self, view, training_example):
        self.view = view
        self.training_example = training_example

        # TODO: change the tuples below so that they are
        #       retreived from the database
        self.properties = [
            Property.create_string("Collected By", ("Sean", "Venkata")),
            Property.create_integer("Number of Rocks", (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)),
            Property.create_string("Light Level: ", ("Bright", "Dark"))
        ]

        for p in self.properties:
            self.view.add_property(p)

        #TODO: property value should be initialized according to the training example..

class TrainingExampleEditorController:

    def __init__(self, view, training_example):
        self.view = view
        self.training_example = training_example
        self.labeling_ctrl = LabelingEditorController(self.view.labeling_view, training_example)
        self.properties_ctrl = PropertyEditorController(self.view.properties_view, training_example)

class Controller:

    def __init__(self, view):
        self.view = view
        image = cv.imread('image.jpg', cv.IMREAD_COLOR)
        training_example = TrainingExample(image)
        self.editor_ctrl = TrainingExampleEditorController(self.view.editor_view, training_example)
