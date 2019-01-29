import Tkinter as tk
from PIL import Image
from PIL import ImageTk
import tkFileDialog
import cv2 as cv


class CollectionGUI(tk.Frame):

    def __init__(self, parent, camera, database, *args, **kwargs):
        # Forward arguments to parent widget's constructor
        tk.Frame.__init__(self, *args, **kwargs)

        self.parent = parent
        self.database = database
        self.directory = tkFileDialog.askdirectory()

        self.__create_widgets()
        self.__layout_widgets()

    def __create_widgets(self):
        self.lblTitle = tk.Label(self, text='Graphical Camera Interface', font=('Helvetica', 20))
        self.lblDirectory = tk.Label(self, text='Directory:')
        self.lblImage(self)

        self.entryDirectory = tk.Entry(self, text=self.directory)

        self.butCaptureFrame = tk.Button(self, text='Capture Frame')

    def __layout_widgets(self):
        self.lblTitle.grid(row=0, column=0)
        self.lblDirectory.grid(row=1, column=0)
        self.lblImage.grid(row=2, column=0, columnspan=2)

        self.entryDirectory.grid(row=1, column=1)

        self.butCaptureFrame.grid(row=3, columnspan=2, sticky='we')

    def __configure_callbacks(self):
        self.parent.after(1, self.update_image)

    def update_image(self):
        if camera.good():
            # Grab frame from camera
            self.image = camera.get_frame()

            # Transform image to format recognized by GUI
            im = cv.cvtColor(self.image, cv.COLOR_BGB2RGB)
            im = Image.fromarray(im)
            im = ImageTk.PhotoImage(im)

            # Display the image
            self.lblImage.config(image=im)
        else:
            self.lblImage.config(text="Camera Failure")


root = tk.Tk()
database = None
camera = Camera()
gui = CollectionGUI(root, camera, database)
