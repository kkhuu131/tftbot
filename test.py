import time

import cv2
import numpy as np
import win32api
from PIL import Image, ImageDraw

from TFTapi import sct


def carousel(target_items):
    method = cv2.TM_SQDIFF_NORMED
    threshold = 0.15

    for item in target_items:
        item_img = get_item_img(item)

        w, h = 480, 360
        img = Image.frombytes('RGB', (w, h), sct.grab({'top': 246, 'left': 707, 'width': w, 'height': h}).rgb)
        lum_img = Image.new('L', (w, h), 0)
        draw = ImageDraw.Draw(lum_img)

        draw.pieslice(((0, 0), (w, h)), 0, 360, fill=255)
        img_arr = np.array(img)
        lum_img_arr = np.array(lum_img)
        final_img_arr = np.dstack((img_arr, lum_img_arr))

        screen = cv2.cvtColor(final_img_arr, cv2.COLOR_RGB2BGR)
        result = cv2.matchTemplate(item_img, screen, method)

        mn, _, mnLoc, _ = cv2.minMaxLoc(result)

        MPx, MPy = mnLoc

        trows, tcols = item_img.shape[:2]

        print("searching for " + item)

        if mn <= threshold:
            print("found " + item)
            x, y = MPx + 707 + int(tcols / 2), MPy + 246 + int(trows / 2)
            move(x, y)
            center_x, center_y = 947, 700
            diff_x, diff_y = x - center_x, y - center_y
            diff_x, diff_y = diff_x * 0.8, diff_y * 0.8
            move(int(center_x + diff_x), int(center_y + diff_y))
            time.sleep(0.1)
            break


def move(x, y):
    win32api.SetCursorPos((x, y))


# private function, returns image of requested item
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


carousel(["glove"])

