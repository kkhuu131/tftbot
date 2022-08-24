import numpy as np
import cv2
from mss import mss
from PIL import Image
from pynput.keyboard import Controller
import win32api, win32con
import keyboard as keyRead
import time

import pytesseract

sct = mss()
keyboard = Controller()
rerollKey = "d"
method = cv2.TM_SQDIFF_NORMED
shop = {'top': 915, 'left': 480, 'width': 1000, 'height': 165}
threshold = 0.2
countdown = 5
gold = 0
goldWindow = {'top': 865, 'left': 820, 'width': 100, 'height': 50}


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(0.1)


def getUnitImg(unit):
    return {
        'senna': cv2.imread('senna.png'),
        'taric': cv2.imread('taric.png'),
        'test': cv2.imread('sett.png'),
        'tristana': cv2.imread('tristana.png')
    }.get(unit, cv2.imread('senna.png'))


def getGold():
    img = Image.frombytes('RGB', (100, 50), sct.grab(goldWindow).rgb)
    screen = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return pytesseract.image_to_string(img)


def buy_out_shop(unit):
    unitImg = getUnitImg(unit)

    while 1:
        img = Image.frombytes('RGB', (1000, 165), sct.grab(shop).rgb)
        screen = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(unitImg, screen, method)

        # We want the minimum squared difference
        mn, _, mnLoc, _ = cv2.minMaxLoc(result)

        MPx, MPy = mnLoc

        trows, tcols = unitImg.shape[:2]

        if mn <= threshold:
            click(MPx + 480 + int(tcols / 2), MPy + 915 + int(trows / 2))
            print('Bought unit')
        else:
            break


def buy_unit(unit):
    unitImg = getUnitImg(unit)

    while 1:
        img = Image.frombytes('RGB', (1000, 165), sct.grab(shop).rgb)
        screen = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(unitImg, screen, method)

        # We want the minimum squared difference
        mn, _, mnLoc, _ = cv2.minMaxLoc(result)

        MPx, MPy = mnLoc

        trows, tcols = unitImg.shape[:2]

        if mn <= threshold:
            click(MPx + 480 + int(tcols / 2), MPy + 915 + int(trows / 2))
            return True
        else:
            return False


# Hold 'q' to pause rolldown, 'p' to unpause
def rolldown(unit):
    paused = False
    while True:
        if not paused:
            buy_out_shop(unit)
            time.sleep(0.1)
            keyRead.press('d')
            time.sleep(0.1)
            keyRead.release('d')
        if keyRead.is_pressed('p'):
            if paused:
                print("Unpaused")
            paused = False
        if keyRead.is_pressed('q'):
            if not paused:
                print("Paused")
            paused = True




def rolldown_startup():

    print("Press 'p' to start")
    keyRead.wait('p')

    print("Press 'q' to stop")

    rolldown('test')
