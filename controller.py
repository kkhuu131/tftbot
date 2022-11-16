import keyboard
import time
import win32api
import win32con
import pyautogui

# Set TFT key binds
roll_key = 'd'
level_key = 'f'
sell_key = 'e'


def move_mouse(coordinate: tuple):
    win32api.SetCursorPos(coordinate)


def roll():
    """Rolls the shop once."""
    keyboard.press(roll_key)
    time.sleep(0.1)
    keyboard.release(roll_key)


def level_up():
    """Presses the level up button once."""
    time.sleep(0.1)
    keyboard.press(level_key)
    time.sleep(0.1)
    keyboard.release(level_key)


def sell():
    """Presses the sell button."""
    keyboard.press(sell_key)
    time.sleep(0.1)
    keyboard.release(sell_key)


def click(coordinate: tuple):
    """Moves cursor to the x,y coordinate and clicks once."""
    move_mouse(coordinate)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, coordinate[0], coordinate[1], 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, coordinate[0], coordinate[1], 0, 0)
    time.sleep(0.1)


def move(coordinate: tuple):
    """Moves cursor to the x,y coordinate."""
    move_mouse(coordinate)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, coordinate[0], coordinate[1], 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, coordinate[0], coordinate[1], 0, 0)


def drag(c1: tuple, c2: tuple):
    """Moves cursor to the x1,y1 coordinate and drag to the x2,y2 coordinate."""
    pyautogui.moveTo(c1[0], c1[1])
    pyautogui.dragTo(c2[0], c2[1], button="left", duration=0.2)


