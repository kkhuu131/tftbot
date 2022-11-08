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


def gold():
    """Reads the screen to determine the current amount of gold and returns it."""
    img = Image.frombytes('RGB', (50, 30), sct.grab({'top': 880, 'left': 868, 'width': 50, 'height': 30}).rgb)
    img = img.resize((80*4, 50*4))
    if ''.join(s for s in pytesseract.image_to_string(img, config='--psm 6') if s.isdigit()) != '':
        return int(''.join(s for s in pytesseract.image_to_string(img, config='--psm 6') if s.isdigit() ))
    else:
        return -1


# augments occur at stage 1-3, 3-5, 5-1
# creeps occur at stage 1-2, 1-3, 1-4, 2-7, 3-7, 4-7 (dragon treasure), 5-7, 6-7, 7-7
# carousels occur at stage 1-1, 2-4, 3-4, 4-4, 5-4, 6-4, 7-4
def stage():
    """Reads the screen to determine the current stage (post stage 1) and returns it as an integer
    (i.e. 2-5 will be 25)."""
    img = Image.frombytes('RGB', (100, 40), sct.grab({'top': 5, 'left': 749, 'width': 100, 'height': 40}).rgb)
    img = img.resize((100 * 4, 40 * 4))
    if ''.join(s for s in pytesseract.image_to_string(img, config='--psm 6') if s.isdigit()) != '':
        return int(''.join(s for s in pytesseract.image_to_string(img, config='--psm 6') if s.isdigit()))
    else:
        return -1


def early_stage():
    """Reads the screen to determine the current stage (only works for stage 1) and returns it."""
    img = Image.frombytes('RGB', (90, 30), sct.grab({'top': 5, 'left': 800, 'width': 90, 'height': 30}).rgb)
    img = img.resize((90 * 4, 30 * 4))
    if ''.join(s for s in pytesseract.image_to_string(img, config='--psm 6') if s.isdigit()) != '':
        return int(''.join(s for s in pytesseract.image_to_string(img, config='--psm 6') if s.isdigit()))
    else:
        return -1


def level():
    """Reads the screen to determine the current level and returns it."""
    img = Image.frombytes('RGB', (30, 30), sct.grab({'top': 880, 'left': 314, 'width': 30, 'height': 30}).rgb)
    if ''.join(s for s in pytesseract.image_to_string(img, config='--psm 6') if s.isdigit()) != '':
        return int(''.join(s for s in pytesseract.image_to_string(img, config='--psm 6') if s.isdigit()))
    else:
        return -1


# Set TFT key binds
roll_key = 'd'
level_key = 'f'
sell_key = 'e'


def roll():
    """Rolls the shop once."""
    keyboard.press(roll_key)
    time.sleep(0.1)
    keyboard.release(roll_key)


def level_up():
    """Presses the level up button once."""
    time.sleep(0.1)
    keyboard.press(level_key)
    time.sleep(0.2)
    keyboard.release(level_key)


def next_level():
    """Determines amount of level ups needed to advance to the next level and performs the action if there is
    sufficient gold. Returns true only if level up was successful."""
    img = Image.frombytes('RGB', (44, 21), sct.grab({'top': 888, 'left': 405, 'width': 44, 'height': 21}).rgb)
    img = img.resize((176, 84))

    config = '--psm 6 -c tessedit_char_whitelist="0123456789/"'
    string = pytesseract.image_to_string(img, config=config)
    string = string.replace('\n', '')
    exp_info = string.split('/')

    if gold() >= math.ceil((int(exp_info[1])-int(exp_info[0]))/4)*4:
        for n in range(math.ceil((int(exp_info[1]) - int(exp_info[0])) / 4)):
            level_up()
        return True
    else:
        return False


def sell():
    """Presses the sell button."""
    time.sleep(0.2)
    keyboard.press(sell_key)
    time.sleep(0.2)
    keyboard.release(sell_key)


def click(x, y):
    """Moves cursor to the x,y coordinate and clicks once."""
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(0.1)


def move(x, y):
    """Moves cursor to the x,y coordinate."""
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)


def drag(x1, y1, x2, y2):
    """Moves cursor to the x1,y1 coordinate and drag to the x2,y2 coordinate."""
    pyautogui.moveTo(x1,y1)
    pyautogui.dragTo(x2,y2, button="left", duration=0.2)


def read_augments():
    """Reads the screen for the augment choices and returns a list of strings representing the augment choices."""
    augments = []
    for x in range(3):
        img = Image.frombytes('RGB', (212, 31), sct.grab({'top': 578, 'left': 442+x*418, 'width': 212, 'height': 31}).rgb)
        augments.append(''.join(s for s in pytesseract.image_to_string(img, config='--psm 6') if s != '\n'))

    return augments


# based on number given, will select one of three augments
# n: 0-2
def pick_augment(n):
    """Given an integer 0, 1, or 2, select the according augment on the screen."""

    if n == 0:
        click(544, 540)
    if n == 1:
        click(957, 540)
    if n == 2:
        click(1371, 540)


# presses reroll augment button
def reroll_augment():
    """Rerolls the augment choices once. Precondition: Have a reroll left."""

    click(965,  869)


# private function, returns image of requested unit
def get_unit_img(unit):
    """Given a unit name, returns the according cv2 image object."""

    return {
        'sett': cv2.imread('images/shop_units/sett.png'),
        'hecarim': cv2.imread('images/shop_units/hecarim.png'),
        'xayah': cv2.imread('images/shop_units/xayah.png'),
        'shen': cv2.imread('images/shop_units/shen.png'),
        'kayn': cv2.imread('images/shop_units/kayn.png'),
        'shyvana': cv2.imread('images/shop_units/shyvana.png'),
        'swain': cv2.imread('images/shop_units/swain.png'),
        'senna': cv2.imread('images/shop_units/senna.png'),
        'taric': cv2.imread('images/shop_units/taric.png'),
        'test': cv2.imread('images/shop_units/sett.png'),
        'kong': cv2.imread('images/shop_units/wukong.png'),
        'ab': cv2.imread('images/shop_units/jax.png'),
        'shi': cv2.imread('images/shop_units/soy.png'),
        'gnar': cv2.imread('images/shop_units/gnar.png'),
        'olaf': cv2.imread('images/shop_units/olaf.png'),
        'yone': cv2.imread('images/shop_units/yone.png'),
        'karma': cv2.imread('images/shop_units/karma.png'),
        'jayce': cv2.imread('images/shop_units/jayce.png'),
        'nidalee': cv2.imread('images/shop_units/nidalee.png'),
        'skarn': cv2.imread('images/shop_units/skarner.png'),
        'viad': cv2.imread('images/shop_units/vladimir.png'),
        'lux': cv2.imread('images/shop_units/lux.png'),
        'varus': cv2.imread('images/shop_units/varus.png'),
        'sylas': cv2.imread('images/shop_units/sylas.png')

    }.get(unit, cv2.imread('images/shop_units/wukong.png'))


shopWindow = {'top': 915, 'left': 480, 'width': 1000, 'height': 165}


def buy_unit(unit):
    """Buys out 1 instance of unit in shop (if one exists)."""
    method = cv2.TM_SQDIFF_NORMED
    threshold = 0.2

    unit_img = get_unit_img(unit)

    while 1:
        img = Image.frombytes('RGB', (1000, 165), sct.grab(shopWindow).rgb)
        screen = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(unit_img, screen, method)

        # We want the minimum squared difference
        mn, _, mnLoc, _ = cv2.minMaxLoc(result)

        MPx, MPy = mnLoc

        trows, tcols = unit_img.shape[:2]

        if mn <= threshold:
            click(MPx + 480 + int(tcols / 2), MPy + 915 + int(trows / 2))
            return True
        else:
            return False


def buy_out_unit(unit):
    """Buys out all instances of unit in shop (if any exists)."""
    method = cv2.TM_SQDIFF_NORMED
    threshold = 0.2

    unit_img = get_unit_img(unit)

    while 1:
        img = Image.frombytes('RGB', (1000, 165), sct.grab(shopWindow).rgb)
        screen = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(unit_img, screen, method)

        # We want the minimum squared difference
        mn, _, mnLoc, _ = cv2.minMaxLoc(result)

        MPx, MPy = mnLoc

        trows, tcols = unit_img.shape[:2]

        if mn <= threshold:
            click(MPx + 480 + int(tcols / 2), MPy + 915 + int(trows / 2))
        else:
            break


def buy_out_units(units, amount):
    """Buys out all instances of each unit in shop (if any exists)."""
    method = cv2.TM_SQDIFF_NORMED
    threshold = 0.13

    shop_slots = [True, True, True, True, True]
    slots_price = [-1, -1, -1, -1, -1]

    for i in range(5):
        price = get_shop_slot_cost(i)
        if price != -1:
            shop_slots[i] = False
            slots_price[i] = price

    unit_img = []
    for unit in units:
        unit_img.append(get_unit_img(unit))

    begin = time.time()
    while time.time() - begin <= 2:
        for i in range(len(unit_img)):
            if amount[i] > 0:
                while 1:
                    img = Image.frombytes('RGB', (1000, 165), sct.grab(shopWindow).rgb)
                    screen = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

                    result = cv2.matchTemplate(unit_img[i], screen, method)

                    # We want the minimum squared difference
                    mn, _, mnLoc, _ = cv2.minMaxLoc(result)

                    MPx, MPy = mnLoc

                    trows, tcols = unit_img[i].shape[:2]

                    if mn <= threshold:
                        if slots_price[x_to_slot(MPx)] != -1 and gold() >= slots_price[x_to_slot(MPx)]:
                            click(MPx + 480 + int(tcols / 2), MPy + 915 + int(trows / 2))
                            amount[i] = amount[i] - 1
                            shop_slots[x_to_slot(MPx)] = False
                            slots_price[x_to_slot(MPx)] = -1
                            time.sleep(0.1)
                        else:
                            break
                    else:
                        break
    return slots_price


def x_to_slot(x):
    """Given an x coordinate, returns the associated shop slot (0-4) corresponding to it. Returns -1 if invalid."""
    if 484 <= x < 685:
        return 0
    if 685 <= x < 889:
        return 1
    if 889 <= x < 1090:
        return 2
    if 1090 <= x < 1291:
        return 3
    if 1291 <= x < 1472:
        return 4
    return -1


def get_bench_pos(n):
    """Return x, y position of given bench slot (only valid from 0-8) (0-indexed, left to right)."""
    if 0 <= n <= 8:
        return 423+n*117, 760
    return 0, 0


def get_board_pos(col, row):
    """Return x, y position of given board slot. col and row counts starting from 0, left to right, top to bottom.
    col: 0-6
    row: 0-3
    """
    if col < 0 or col > 6 or row < 0 or row > 3:
        raise Exception(str(col) + "," + str(row) + " is not a valid board position")
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


def get_items_pos(n):
    """Return x, y position of given item slot. Only valid from 0-9."""
    item_locations = [[289, 753], [335, 721], [296, 687], [352, 673], [411, 673], [448, 631], [378, 627], [313, 631],
                      [334, 586], [393, 586]]
    return item_locations[n][0], item_locations[n][1]


def field_unit(bench_slot, col, row):
    """Fields a unit from given slot from bench to col,row position on board."""
    x1, y1 = get_bench_pos(bench_slot)
    x2, y2 = get_board_pos(col, row)
    drag(x1, y1, x2, y2)


def bench_unit(bench_slot, col, row):
    """Benches a unit from col,row position on board to given slot from bench."""
    x1, y1 = get_bench_pos(bench_slot)
    x2, y2 = get_board_pos(col, row)
    drag(x2, y2, x1, y1)


def move_unit(col1, row1, col2, row2):
    """Moves a unit from col1,row1 position on board to col2,row2 position on board."""
    x1, y1 = get_board_pos(col1, row1)
    x2, y2 = get_board_pos(col2, row2)
    drag(x1, y1, x2, y2)


def carousel(target_items, stage_number):
    """Given a list of items and stage number, attempt to get the highest priority item possible on carousel."""
    method = cv2.TM_SQDIFF_NORMED
    threshold = 0.15
    timeout = 30
    min_duration = 7
    begin = time.time()

    while time.time() - begin <= min_duration:
        for item in target_items:

            if stage_number == 11:
                while early_stage() != stage_number+1 and time.time() - begin <= timeout:
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

                    if mn <= threshold:
                        x, y = MPx + 707 + int(tcols / 2), MPy + 246 + int(trows / 2)
                        center_x, center_y = 947, 700
                        diff_x, diff_y = x - center_x, y - center_y
                        diff_x, diff_y = diff_x * 0.8, diff_y * 0.8
                        move(int(center_x + diff_x), int(center_y + diff_y))
                        time.sleep(0.1)
                    else:
                        break
            else:
                while stage() != stage_number + 1 and time.time() - begin <= timeout:
                    item_img = get_item_img(item)

                    w, h = 480, 360
                    img = Image.frombytes('RGB', (w, h),
                                          sct.grab({'top': 246, 'left': 707, 'width': w, 'height': h}).rgb)
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

                    if mn <= threshold:
                        x, y = MPx + 707 + int(tcols / 2), MPy + 246 + int(trows / 2)
                        center_x, center_y = 947, 700
                        diff_x, diff_y = x - center_x, y - center_y
                        diff_x, diff_y = diff_x * 0.8, diff_y * 0.8
                        move(int(center_x + diff_x), int(center_y + diff_y))
                        time.sleep(0.1)
                    else:
                        break


# private function, returns image of requested item
def get_item_img(item):
    """Given an item name, returns the corresponding cv2 image object."""
    return {
        'belt': cv2.imread('images/carousel_items/carousel_belt.png'),
        'bow': cv2.imread('images/carousel_items/carousel_bow.png'),
        'cloak': cv2.imread('images/carousel_items/carousel_cloak.png'),
        'glove': cv2.imread('images/carousel_items/carousel_glove.png'),
        'needless': cv2.imread('images/carousel_items/carousel_rod.png'),
        'sword': cv2.imread('images/carousel_items/carousel_sword.png'),
        'tear': cv2.imread('images/carousel_items/carousel_tear.png'),
        'vest': cv2.imread('images/carousel_items/carousel_vest.png')

    }.get(item, cv2.imread('images/carousel_items/carousel_belt.png'))


def lock_shop():
    """Locks the shop. Unlocks if shop is already locked."""
    click(1452, 901)


def collect_items(secs, hard_stop):
    """Collects all the drops on the board."""
    method = cv2.TM_SQDIFF_NORMED
    threshold = 0.15

    drop_img = [cv2.imread('images/misc/grey_drop.png'), cv2.imread('images/misc/blue_drop.png'), cv2.imread('images/misc/gold_drop.png')]
    board_window = {'top': 164, 'left': 501, 'width': 914, 'height': 555}

    time_start = time.time()
    current_stage = stage()
    while time.time()-time_start <= secs:
        if hard_stop:
            read_stage = stage()
            if read_stage % 10 == 1 and int(read_stage/10) == int(current_stage/10) + 1:
                break
        for i in range(len(drop_img)):
            while 1:
                img = Image.frombytes('RGB', (914, 555), sct.grab(board_window).rgb)
                screen = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

                result = cv2.matchTemplate(drop_img[i], screen, method)

                # We want the minimum squared difference
                mn, _, mnLoc, _ = cv2.minMaxLoc(result)

                MPx, MPy = mnLoc

                trows, tcols = drop_img[i].shape[:2]

                if mn <= threshold:
                    move(MPx + 501 + int(tcols / 2), MPy + 164 + int(trows / 2))
                    time.sleep(0.3)
                else:
                    break


def items():
    """Scans items on screen and return String list of item names"""
    item_locations = [[289, 753], [335, 721], [296, 687], [352, 673], [411, 673], [448, 631], [378, 627], [313, 631], [334, 586], [393, 586]]
    item_inventory = ["", "", "", "", "", "", "", "", "", ""]
    for i in range(10):
        time.sleep(0.4)
        win32api.SetCursorPos((item_locations[i][0], item_locations[i][1]))
        time.sleep(0.4)
        img = Image.frombytes('RGB', (170, 30), sct.grab(
            {'top': item_locations[i][1] + 40, 'left': item_locations[i][0] + 100, 'width': 170, 'height': 30}).rgb)

        item_name = (''.join(s for s in pytesseract.image_to_string(img, config='--psm 6') if s.isalpha()))
        item_name = ' '.join([w for w in item_name.split() if len(w)>3 or w == 'of'])
        if item_name != '' and item_name[0].isupper():
            item_inventory[i] = (''.join(s for s in pytesseract.image_to_string(img, config='--psm 6') if s != '\n'))

    return item_inventory


def bench():
    """Scans bench on screen and return String list of unit names"""
    new_bench = ["", "", "", "", "", "", "", "", "", ""]
    for n in range(9):
        click(1000, 300)
        x, y = get_bench_pos(n)
        move(x, y)
        time.sleep(0.05)
        img = Image.frombytes('RGB', (100, 24), sct.grab(
            {'top': y - 68, 'left': x + 200 + n * 8, 'width': 100, 'height': 24}).rgb)
        img = img.resize((100 * 4, 24 * 4))
        unit_name = (''.join(s for s in pytesseract.image_to_string(img, config='--psm 6') if s.isalpha()))
        unit_name = ' '.join([w for w in unit_name.split() if len(w) > 2])

        if unit_name != '':
            start = 0
            for s in unit_name:
                if s.islower():
                    start = start + 1
                else:
                    break

            unit_name = unit_name[start::]
            new_bench[n] = unit_name
    endx, endy = get_board_pos(4, 2)
    move(endx,endy)
    return new_bench


def unit_name_on_board(col, row):
    """Scans col,row position of board and returns the unit name of the unit there."""
    x,y = get_board_pos(col, row)
    move(x, y)
    time.sleep(0.2)
    img = Image.frombytes('RGB', (120, 24), sct.grab(
        {'top': y - 70, 'left': x + 200, 'width': 120, 'height': 24}).rgb)

    unit_name = (''.join(s for s in pytesseract.image_to_string(img, config='--psm 6') if s.isalpha()))
    unit_name = ' '.join([w for w in unit_name.split() if len(w) > 2])

    if unit_name != '':
        start = 0
        for s in unit_name:
            if s.islower():
                start = start + 1
            else:
                break

        unit_name = unit_name[start::]

    return unit_name


def clear_bench(units, amount):
    """Given a list of units and requested amounts, sell irrelevant units, return first slot (left to right)
    that will be empty by the end."""
    first_empty_slot = -1
    for n in range(9):
        click(1000, 300)
        x, y = get_bench_pos(n)
        move(x, y)
        time.sleep(0.1)
        img = Image.frombytes('RGB', (120, 24), sct.grab(
            {'top': y - 70, 'left': x + 200, 'width': 120, 'height': 24}).rgb)

        unit_name = ''.join(s for s in pytesseract.image_to_string(img, config='--psm 6') if s.isalpha())
        unit_name = ' '.join([w for w in unit_name.split() if len(w) > 2])

        if unit_name != '':
            sell_unit = True

            for i in range(len(units)):
                if units[i].lower() in unit_name.lower() and amount[i] > 0:
                    sell_unit = False
                    break

            if sell_unit:
                if first_empty_slot != -1:
                    first_empty_slot = n
                x, y = get_bench_pos(n)
                win32api.SetCursorPos((x, y))
                time.sleep(0.1)
                sell()
        else:
            if first_empty_slot != -1:
                first_empty_slot = n

    endx, endy = get_board_pos(4, 2)
    move(endx, endy)
    return first_empty_slot


def unbench_unit(current_bench, unit, col, row):
    """Given the current bench, unit name, and col,row board position, field the unit from the bench to the position.
    Return the bench slot that we unbenched the unit from. Return -1 if not found."""
    i = search_bench(current_bench, unit)
    if i != -1:
        x1, y1 = get_bench_pos(i)
        x2, y2 = get_board_pos(col, row)
        drag(x1, y1, x2, y2)
        current_bench[i] = ""
        return i
    return -1


def buy_slot(n):
    """Buy the unit on the given shop slot."""
    if n < 0 or n > 4:
        raise Exception(str(n) + " is not between 0 and 4")
    time.sleep(0.1)
    click(576+n*204, 994)
    time.sleep(0.1)


def search_bench(bench, unit):
    """Searches the given bench for the given unit. Return the bench slot that contains unit, and -1 if not found."""
    for i in range(len(bench)):
        if unit.lower() in bench[i].lower():
            return i
    return -1


def amount_of_unit_on_bench(bench, unit):
    """Counts the number of the given unit that are on the given bench."""
    count = 0
    for i in range(len(bench)):
        if unit.lower() in bench[i].lower():
            count = count + 1
    return count


def accept_queue():
    """Accepts queue until game starts."""
    method = cv2.TM_SQDIFF_NORMED
    threshold = 0.2

    accept_img = cv2.imread("images/misc/accept_queue.png")

    while not wait_until_game_start():
        img = Image.frombytes('RGB', (1920, 1080), sct.grab({'top': 0, 'left': 0, 'width': 1920, 'height': 1080}).rgb)
        screen = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(accept_img, screen, method)

        # We want the minimum squared difference
        mn, _, mnLoc, _ = cv2.minMaxLoc(result)

        MPx, MPy = mnLoc

        trows, tcols = accept_img.shape[:2]

        if mn <= threshold:
            click(MPx + int(tcols / 2), MPy + int(trows / 2))


def get_shop_slot_cost(n):
    """Returns the cost of the unit at the bench slot n (0-4)."""
    if 0 <= n <= 4:
        img = Image.frombytes('RGB', (24, 22), sct.grab({'top': 1043, 'left': 648+n*201, 'width': 24, 'height': 22}).rgb)
        img = img.resize((24 * 4, 22 * 4))
        if ''.join(s for s in pytesseract.image_to_string(img, config='--psm 6') if s.isdigit()) != '':
            return int(''.join(s for s in pytesseract.image_to_string(img, config='--psm 6') if s.isdigit()))
    return -1


def wait_until_game_start():
    """Pauses program until the game starts."""
    method = cv2.TM_SQDIFF_NORMED
    threshold = 0.1
    img = Image.frombytes('RGB', (90, 30), sct.grab({'top': 5, 'left': 800, 'width': 90, 'height': 30}).rgb)
    start_stage_img = cv2.imread("images/misc/start_stage.png")
    screen = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    result = cv2.matchTemplate(start_stage_img, screen, method)

    # We want the minimum squared difference
    mn, _, mnLoc, _ = cv2.minMaxLoc(result)

    return mn <= threshold




