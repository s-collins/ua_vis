import Tkinter as tk
import ttk
import cv2 as cv
from PIL import Image, ImageTk


class View(tk.Frame):

    def __init__(self, master, controller, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.controller = controller

        # create notebook
        self.notebook = ttk.Notebook(self)

        # create tabs
        self.edit_tab = EditTab(self.notebook, controller)

        # add the tabs
        self.notebook.add(self.edit_tab, text='Edit')

        self.__layout()

    def __layout(self):
        self.notebook.grid()


# -----------------------------------------------------------------------------------------------------------------------
# CAPTURE TAB
# -----------------------------------------------------------------------------------------------------------------------


class CaptureTab(tk.Frame):

    def __init__(self, master, controller, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.controller = controller



# -----------------------------------------------------------------------------------------------------------------------
# EDIT TAB
# -----------------------------------------------------------------------------------------------------------------------


class EditTab(tk.Frame):

    def __init__(self, master, controller, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.controller = controller
        self.labeler = Labeler(self, controller)
        self.property_editor = PropertyEditor(self, controller)
        self.__layout()

    def __layout(self):
        self.labeler.grid(row=0, column=0)
        self.property_editor.grid(row=0, column=1, sticky='n')


class Labeler(tk.Frame):

    def __init__(self, master, controller, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.controller = controller
        self.label_frame = tk.LabelFrame(self, text='Labeler', padx=10, pady=10)
        self.image = tk.Label(self.label_frame)
        self.listbox = tk.Listbox(self.label_frame, height=10, selectbackground='Blue', selectforeground='White')
        self.button = tk.Button(self.label_frame, text='Remove Selected')
        self.__layout()
        self.__config_callbacks()

    def __layout(self):
        self.label_frame.grid(padx=10, pady=10, sticky='nswe')
        self.image.grid(row=0, column=0)
        self.listbox.grid(row=1, column=0, sticky='we')
        self.button.grid(row=2, column=0, sticky='we')

    # TODO: implement
    def __config_callbacks(self):
        pass

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

