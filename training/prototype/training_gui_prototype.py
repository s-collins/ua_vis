import Tkinter as tk
from PIL import Image
from PIL import ImageTk
import tkFileDialog
import cv2 as cv
from camera import *

# Dialog to open a file
#path = tkFileDialog.askopenfilename()

camera = Camera()

if camera.good():
    root = tk.Tk()

    # Get image and convert to appropriate format
    image = camera.get_frame()
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)

    # Add the image panel
    panel = tk.Label(root, image=image)
    panel.image = image
    panel.grid(row=0)

    btn = tk.Button(root, text='Test Button')
    btn.grid(row=1, sticky='we')

    root.mainloop()
