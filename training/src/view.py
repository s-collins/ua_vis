import Tkinter as tk
import ttk
import cv2 as cv
from PIL import Image, ImageTk
import copy


class View(tk.Frame):

    def __init__(self, master, controller, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.controller = controller

        # create notebook
        self.notebook = ttk.Notebook(self)

        # create tabs
        self.project_tab = ProjectTab(self.notebook, controller)
        self.capture_tab = CaptureTab(self.notebook, controller)
        self.edit_tab = EditTab(self.notebook, controller)

        # add the tabs
        self.notebook.add(self.project_tab, text='Project')
        self.notebook.add(self.capture_tab, text='Capture')
        self.notebook.add(self.edit_tab, text='Edit')

        self.__layout()
        self.__configure_callbacks()

    def __layout(self):
        self.notebook.grid()

    def __configure_callbacks(self):
        self.notebook.bind('<<NotebookTabChanged>>', self.resize_tab)

    def resize_tab(self, event):
        event.widget.update_idletasks()
        tab = event.widget.nametowidget(event.widget.select())
        event.widget.configure(height=tab.winfo_reqheight(), width=tab.winfo_reqwidth())


# -----------------------------------------------------------------------------------------------------------------------
# PROJECT TAB
# -----------------------------------------------------------------------------------------------------------------------


class ProjectTab(tk.Frame):

    def __init__(self, master, controller, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.controller = controller

        self.selection_frame = tk.LabelFrame(self, text='Select Project', padx=10, pady=10)
        self.label1 = tk.Label(self.selection_frame, text='Current Project:')

        self.creation_frame = tk.LabelFrame(self, text='Create Project', padx=10, pady=10)
        self.label2 = tk.Label(self.creation_frame, text='Name of Project:')
        self.project_name_entry = tk.Entry(self.creation_frame)
        self.create_button = tk.Button(self.creation_frame, text='Create')

        self.__layout()
        self.__configure_callbacks()

    def __layout(self):
        self.selection_frame.grid(row=0, column=0, padx=10, pady=10, sticky='we')
        self.label1.pack(anchor='w')
        self.creation_frame.grid(row=1, column=0, padx=10, pady=10, sticky='we')
        self.label2.pack(anchor='w')
        self.project_name_entry.pack(fill=tk.BOTH, expand=True)
        self.create_button.pack(fill=tk.BOTH, expand=True)

    def __configure_callbacks(self):
        pass

    def set_model(self, model):
        self.model = model

    def notify(self):
        options = self.model.get_project_list()
        selected = tk.StringVar(self)
        index = self.model.get_selected_index()
        if index is not None:
            selected.set(options[index])
        self.projects_menu = apply(tk.OptionMenu, (self.selection_frame, selected) + tuple(options))
        self.projects_menu.pack(fill=tk.BOTH)


# -----------------------------------------------------------------------------------------------------------------------
# CAPTURE TAB
# -----------------------------------------------------------------------------------------------------------------------


class CaptureTab(tk.Frame):

    def __init__(self, master, controller, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.controller = controller

        self.label_frame = tk.LabelFrame(self, text='Camera Feed', padx=10, pady=10)
        self.image_display = tk.Label(self.label_frame)
        self.button = tk.Button(self.label_frame, text='Capture Frame')

        self.__layout()
        self.__configure_callbacks()

    def __layout(self):
        self.label_frame.grid(padx=10, pady=10)
        self.image_display.grid(row=0, column=0)
        self.button.grid(row=1, column=0, sticky='we')

    # TODO: implement me!
    def __configure_callbacks(self):
        self.button.config(command=self.controller.capture_button_click)

    def update_image(self, cv_image):
        im = cv.cvtColor(cv_image, cv.COLOR_BGR2RGB)
        im = Image.fromarray(im)
        im = ImageTk.PhotoImage(im)
        self.image_display.configure(image=im)
        self.image_display.image = im

# -----------------------------------------------------------------------------------------------------------------------
# EDIT TAB
# -----------------------------------------------------------------------------------------------------------------------


class EditTab(tk.Frame):

    def __init__(self, master, controller, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.controller = controller
        self.labeler = Labeler(self, controller)
        self.property_editor = PropertyEditor(self, controller)
        self.save_button = tk.Button(self, text='Save')
        self.model = None
        self.__layout()

    def __layout(self):
        self.labeler.grid(row=0, column=0, rowspan=2)
        self.property_editor.grid(row=0, column=1, sticky='n')
        self.save_button.grid(row=1, column=1, sticky='wes', padx=10, pady=10)

    def set_model(self, model):
        self.model = model

    def notify(self):
        self.labeler.refresh_display(self.model)


class Labeler(tk.Frame):

    CROSS_COLOR = (0, 0, 255)
    LABEL_BOX_COLOR = (0, 255, 0)
    LABEL_BOX_COLOR_SELECTED = (255, 0, 0)

    def __init__(self, master, controller, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.controller = controller
        self.image_frame = tk.LabelFrame(self, text='Image', padx=10, pady=10)
        self.label_frame = tk.LabelFrame(self, text='Labels', padx=10, pady=10)
        self.image = tk.Label(self.image_frame)
        self.listbox = tk.Listbox(self.label_frame, height=6, selectbackground='Blue', selectforeground='White')
        self.button = tk.Button(self.label_frame, text='Remove Selected')
        self.__layout()
        self.__config_callbacks()

    def __layout(self):
        self.image_frame.grid(row=0, column=0, padx=10, pady=10, sticky='we')
        self.image.grid(row=0, column=0)
        self.label_frame.grid(row=1, column=0, padx=10, pady=10, sticky='we')
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.button.pack(fill=tk.BOTH, expand=True)

    def __config_callbacks(self):
        self.image.bind('<Motion>', self.controller.mouse_motion_on_labeling_image_display)
        self.image.bind('<Button-1>', self.controller.mouse_click_on_labeling_image_display)
        self.listbox.bind('<<ListboxSelect>>', self.controller.select_label_in_list)
        self.button.config(command=self.controller.remove_selected_button_click)

    def refresh_display(self, model):
        im = copy.deepcopy(model.get_image())

        # draw the cross
        height, width, channels = im.shape
        (x, y) = model.get_cross()
        line1 = ((0, y), (width, y))
        line2 = ((x, 0), (x, height))
        cv.line(im, line1[0], line1[1], self.CROSS_COLOR)
        cv.line(im, line2[0], line2[1], self.CROSS_COLOR)

        # draw the in-progress label box
        if model.is_box_in_progress():
            pt1 = model.get_box_origin()
            pt2 = model.get_cross()
            cv.rectangle(im, pt1, pt2, self.LABEL_BOX_COLOR, 1)

        # draw the label boxes
        labels = model.get_labels()
        for index, label in enumerate(labels):
            if index == model.get_selection_index():
                cv.rectangle(im, label[0], label[1], self.LABEL_BOX_COLOR_SELECTED, 2)
            else:
                cv.rectangle(im, label[0], label[1], self.LABEL_BOX_COLOR, 2)

        # convert image format from BGR to RGB (for tkinter compatibility)
        im = cv.cvtColor(im, cv.COLOR_BGR2RGB)
        im = Image.fromarray(im)
        im = ImageTk.PhotoImage(im)
        self.image.configure(image=im)
        self.image.image = im

        # Refresh the list of labels
        labels = model.get_labels()
        self.listbox.delete(0, tk.END)
        for label in labels:
            text = str(label[0]) + ', ' + str(label[1])
            self.listbox.insert(tk.END, text)
        index = model.get_selection_index()
        if index is not None:
            self.listbox.selection_set(index)
            self.listbox.activate(index)


class PropertyEditor(tk.Frame):

    def __init__(self, master, controller, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.controller = controller
        self.label_frame = tk.LabelFrame(self, text='Properties', padx=10, pady=10)
        self.labels = []
        self.menus = []
        self.__layout()
        self.__config_callbacks()

    def __layout(self):
        self.label_frame.grid(padx=10, pady=10, sticky='nswe')

    # TODO: implement
    def __config_callbacks(self):
        pass

    def add_property(self, property):
        label = tk.Label(self.label_frame, text=property.title)
        menu = tk.OptionMenu(self.label_frame, property.var, *property.options)
        self.labels.append(label)
        self.menus.append(menu)
        label.grid(row=len(self.labels), column=0, sticky='w')
        menu.grid(row=len(self.menus), column=1, sticky='we')

