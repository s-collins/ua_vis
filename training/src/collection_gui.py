import Tkinter as tk
from PIL import Image
from PIL import ImageTk
import tkFileDialog
import cv2 as cv
from camera import Camera


class CollectionGUI(tk.Frame):

    # Refresh rate [milliseconds]
    REFRESH_RATE = 120

    def __init__(self, parent, camera, database, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.grid()
        self.parent = parent
        self.camera = camera
        self.database = database
        self.directory = tkFileDialog.askdirectory()
        self.__create_widgets()
        self.__layout_widgets()
        self.__configure_callbacks()
        self.update_image()

    def __create_widgets(self):
        self.lblTitle = tk.Label(self, text='Graphical Camera Interface', font=('Helvetica', 20))
        self.lblDirectory = tk.Label(self, text='Directory:')
        self.lblImage = tk.Label(self)
        self.entryDirectory = tk.Entry(self, text=self.directory)
        self.butCaptureFrame = tk.Button(self, text='Capture Frame')

    def __layout_widgets(self):
        self.lblTitle.grid(row=0, column=0, columnspan=2)
        self.lblDirectory.grid(row=1, column=0)
        self.lblImage.grid(row=2, column=0, columnspan=2)
        self.entryDirectory.grid(row=1, column=1)
        self.butCaptureFrame.grid(row=3, columnspan=2, sticky='we')

    def __configure_callbacks(self):
        pass

    def update_image(self):
        if self.camera.good():
            # Grab frame from camera
            self.image = self.camera.get_frame()

            # Transform image to format recognized by GUI
            im = cv.cvtColor(self.image, cv.COLOR_BGR2RGB)
            im = Image.fromarray(im)
            im = ImageTk.PhotoImage(im)

            # Display the image
            self.lblImage.configure(image=im)
            self.lblImage.image = im

        # Refresh the image according to refresh rate
        self.parent.after(CollectionGUI.REFRESH_RATE, self.update_image)


root = tk.Tk()
database = None
camera = Camera()
gui = CollectionGUI(root, camera, database)
root.mainloop()
