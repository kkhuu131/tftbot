import time

import cv2
import keyboard
import numpy as np
import win32api
from PIL import Image, ImageDraw
from pytesseract import pytesseract

from TFTapi import sct


def get_board_pos(col, row):
    x, y = 0, 0
    if row == 0:
        x, y = 562, 410
        x += 114 * col
    if row == 1:
        x, y = 610, 480
        x += 118 * col
    if row == 2:
        x, y = 534, 560
        x += 123 * col
    if row == 3:
        x, y = 581, 670
        x += 128 * col

    return x, y


def get_jade_statue(positions, ignore_positions):
    method = cv2.TM_SQDIFF_NORMED
    threshold = 0.3

    jade_statue_img = cv2.imread('jade_statue.png')

    w, h = 978, 358
    img = Image.frombytes('RGB', (w, h), sct.grab({'top': 382, 'left': 428, 'width': w, 'height': h}).rgb)
    img_array = np.array(img)
    # cover already positioned jades
    for n in range(len(positions)):
        if ignore_positions[n]:
            print("drawing")
            x, y = get_board_pos(positions[n][0], positions[n][1])
            cv2.rectangle(img_array, (x-20-428, y-40-382), (x+20-428, y+40-382), (0, 0, 0), -1)

    screen = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    result = cv2.matchTemplate(jade_statue_img, screen, method)

    # We want the minimum squared difference
    mn, _, mnLoc, _ = cv2.minMaxLoc(result)

    MPx, MPy = mnLoc

    trows, tcols = jade_statue_img.shape[:2]

    if mn <= threshold:
        x1, y1 = MPx + 428 + int(tcols / 2), MPy + 382 + int(trows / 2)
        win32api.SetCursorPos((x1, y1))
        print("found")
    else:
        print("not found")


def early_stage():
    img = Image.frombytes('RGB', (90, 30), sct.grab({'top': 5, 'left': 800, 'width': 90, 'height': 30}).rgb)
    img.show()
    img = img.resize((90 * 4, 30 * 4))
    if ''.join(s for s in pytesseract.image_to_string(img, config='--psm 6') if s.isdigit()) != '':
        return int(''.join(s for s in pytesseract.image_to_string(img, config='--psm 6') if s.isdigit()))
    else:
        return -1

def get_item_img(item):
    return {
        'belt': cv2.imread('carousel_belt.png'),
        'bow': cv2.imread('carousel_bow.png'),
        'cloak': cv2.imread('carousel_cloak.png'),
        'glove': cv2.imread('carousel_glove.png'),
        'needless': cv2.imread('carousel_rod.png'),
        'sword': cv2.imread('carousel_sword.png'),
        'tear': cv2.imread('carousel_tear.png'),
        'vest': cv2.imread('carousel_vest.png')
    }.get(item, cv2.imread('carousel_belt.png'))


item = get_item_img('belt')

