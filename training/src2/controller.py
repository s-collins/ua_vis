import Tkinter as tk
import cv2 as cv
from view import View
from property import Property
from camera import *
from training_example import TrainingExample


class EditTabState:

    def __init__(self):
        self.box_in_progress = False
        self.box_x = None
        self.box_y = None
        self.cross_x = 0
        self.cross_y = 0
        self.training_example = TrainingExample()
        self.views = []
        self.selected_index = None

    def reset(self):
        self.box_in_progress = False
        self.box_x = None
        self.box_y = None
        self.cross_x = 0
        self.cross_y = 0
        self.training_example = TrainingExample()
        self.selected_index = None

    def register(self, view):
        """Registers a view with this object so that it will be notified on changes."""
        self.views.append(view)
        view.set_model(self)

    def notify_all(self):
        for view in self.views:
            view.notify()

    def set_image(self, image):
        self.training_example.image = image
        self.notify_all()

    def set_cross_pos(self, x, y):
        self.cross_x = x
        self.cross_y = y
        self.notify_all()

    def set_box_origin(self, x, y):
        self.box_x = x
        self.box_y = y
        self.box_in_progress = True
        self.notify_all()

    def set_selected_label(self, index):
        self.selected_index = index
        self.notify_all()

    def add_label(self, x, y):
        label = ((self.box_x, self.box_y), (x, y))
        self.training_example.labels.append(label)
        self.box_in_progress = False
        self.box_x = None
        self.box_y = None
        self.notify_all()

    def delete_selected_label(self):
        if self.selected_index is None:
            return
        del self.training_example.labels[self.selected_index]
        if self.selected_index != 0:
            self.selected_index -= 1
        else:
            self.selected_index = None
        self.notify_all()

    def is_box_in_progress(self):
        return self.box_in_progress

    def get_image(self):
        return self.training_example.image

    def get_cross(self):
        return self.cross_x, self.cross_y

    def get_labels(self):
        return self.training_example.labels

    def get_box_origin(self):
        return self.box_x, self.box_y

    def get_selection_index(self):
        return self.selected_index


class Controller:

    REFRESH_RATE = 50

    def __init__(self, camera):

        self.camera = camera

        # Create the view
        self.root = tk.Tk()
        self.root.title('Training Examples')
        self.view = View(self.root, self)
        self.view.edit_tab.property_editor.add_property(Property.create_string('Name', ('Sean', 'Venkata')))
        self.view.edit_tab.property_editor.add_property(Property.create_integer('Number', (1, 2, 3)))
        self.view.grid()

        # Variables to hold state
        self.edit_state = EditTabState()
        self.edit_state.register(self.view.edit_tab)

        self.root.after(self.REFRESH_RATE, self.update_capture_feed)

    def run(self):
        self.root.mainloop()

    def update_capture_feed(self):
        if self.camera.good():
            self.feed = self.camera.get_frame()
            self.view.capture_tab.update_image(self.feed)
        self.root.after(self.REFRESH_RATE, self.update_capture_feed)

    # CALLBACKS

    def capture_button_click(self):
        self.edit_state.reset()
        self.edit_state.set_image(self.feed)

    def mouse_motion_on_labeling_image_display(self, event):
        self.edit_state.set_cross_pos(event.x, event.y)

    def mouse_click_on_labeling_image_display(self, event):
        if self.edit_state.is_box_in_progress():
            self.edit_state.add_label(event.x, event.y)
        else:
            self.edit_state.set_box_origin(event.x, event.y)

    def remove_selected_button_click(self):
        self.edit_state.delete_selected_label()

    def select_label_in_list(self, event):
        self.edit_state.set_selected_label(event.widget.curselection()[0])


#camera = FakeCamera()
camera = Camera()
Controller(camera).run()
