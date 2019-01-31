import Tkinter as tk
import ttk
from PIL import Image, ImageTk
import cv2 as cv


class LabelingEditorView(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # Configure the view
        self.__create_widgets()
        self.__layout_widgets()

    def __create_widgets(self):
        self.sec_labeling = tk.LabelFrame(self, text='Labeling', padx=10, pady=10)
        self.lbl_image = tk.Label(self.sec_labeling)
        self.list = tk.Listbox(self.sec_labeling, height=10, selectbackground="Blue", selectforeground="White")
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


class PropertyEditorView(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.__create_widgets()
        self.__layout_widgets()

    def __create_widgets(self):
        self.sec_form = tk.LabelFrame(self, text='Properties', padx=10, pady=10)
        self.labels = []
        self.menus = []

    def __layout_widgets(self):
        self.sec_form.grid(padx=10, pady=10, sticky='we')

    def add_property(self, property):
        label = tk.Label(self.sec_form, text=property.title)
        menu = tk.OptionMenu(self.sec_form, property.var, *property.options)
        self.labels.append(label)
        self.menus.append(menu)
        label.grid(row=len(self.labels), column=0, sticky='w')
        menu.grid(row=len(self.menus), column=1, sticky='we')


class TrainingExampleEditorView(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.__create_widgets()
        self.__layout_widgets()

    def __create_widgets(self):
        self.labeling_view = LabelingEditorView(self)
        self.properties_view = PropertyEditorView(self)

        self.buttons = tk.Frame(self, padx=10, pady=10)
        self.save_button = tk.Button(self.buttons, text='Save')
        self.cancel_button = tk.Button(self.buttons, text='Cancel')

    def __layout_widgets(self):
        self.labeling_view.grid(row=0, column=0, rowspan=2)
        self.properties_view.grid(row=0, column=1, sticky='nwe')
        self.buttons.grid(row=1, column=1, sticky='es')
        self.save_button.grid(row=0, column=0)
        self.cancel_button.grid(row=0, column=1)

from collection_gui import *
from camera import *

class View(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.__create_widgets()
        self.__layout_widgets()

    def __create_widgets(self):
        self.notebook = ttk.Notebook(self)

        camera = Camera()
        self.capture = CollectionGUI(self, camera, None)
        self.notebook.add(self.capture, text='Capture')

        self.editor_view = TrainingExampleEditorView(self.notebook)
        self.notebook.add(self.editor_view, text='Edit')

    def __layout_widgets(self):
        self.notebook.grid(sticky='nsew')
