import pyautogui
import math
import time
import keyboard
import numpy as np
import cv2
from mss import mss
from PIL import Image, ImageDraw
import win32api
import win32con
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

sct = mss()

img = Image.frombytes('RGB', (74, 23), sct.grab({'top': 1040, 'left': 888, 'width': 74, 'height': 23}).rgb)
img = img.resize((100 * 4, 24 * 4))
unit_name = (''.join(s for s in pytesseract.image_to_string(img, config='--psm 6') if s.isalpha()))
unit_name = ' '.join([w for w in unit_name.split() if len(w) > 2])

print(unit_name)