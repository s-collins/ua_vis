import Tkinter as tk
from PIL import Image
from PIL import ImageTk
import tkFileDialog
import cv2 as cv


class CollectionGUI(tk.Frame):

    def __init__(self, parent, database, *args, **kwargs):
        # Forward arguments to parent widget's constructor
        tk.Frame.__init__(self, *args, **kwargs)

        self.parent = parent
        self.database = database
        self.directory = tkFileDialog.askdirectory()
        print(self.directory)

gui = CollectionGUI()
