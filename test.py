import time

import cv2
import keyboard
import numpy as np
import win32api
import win32con
from PIL import Image, ImageDraw
from pytesseract import pytesseract

from TFTapi import sct
import tkinter as tk

root = tk.Tk()
var = tk.StringVar()
var.set('hello')

label = tk.Label(root, textvariable = var)
label.pack()
root.update_idletasks()

for i in range(6):
    time.sleep(3)
    var.set('goodbye' if i%2 else 'hello')
    root.update_idletasks()

root.mainloop()