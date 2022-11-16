# (top, left, width, height) -> (left, top, right, bottom)

SCREEN_WINDOW = (0, 0, 1920, 1080)

GOLD_WINDOW = (868, 880, 918, 920)

STAGE_WINDOW = (749, 5, 849, 45)

STAGE1_WINDOW = (800, 5, 890, 35)

LEVEL_WINDOW = (314, 880, 344, 910)

LEVEL_EXP_WINDOW = (405, 888, 449, 909)

AUGMENT_NAME_WINDOWS = [
    (442, 578, 654, 609),
    (442+418, 578, 654+418, 609),
    (442+418*2, 578, 654+418*2, 609)
]

AUGMENT_COORDS = [
    (544, 540),
    (957, 540),
    (1371, 540),
]

SHOP_WINDOW = (480, 915, 1480, 1080)

UNIT_NAME_IN_SHOP_WINDOWS = [
    (483, 1040, 583, 1065),
    (684, 1040, 784, 1065),
    (885, 1040, 985, 1065),
    (1087, 1040, 1187, 1065),
    (1288, 1040, 1388, 1065)
]

SHOP_SLOT_COORDS = [
    (585, 988),
    (787, 988),
    (990, 988),
    (1190, 988),
    (1382, 988),
]

BENCH_COORDS = []

for n in range(9):
    BENCH_COORDS.append((423 + n * 117, 760))


UNIT_NAME_ON_BENCH_WINDOWS = []

for n in range(9):
    x, y = BENCH_COORDS[n]
    UNIT_NAME_ON_BENCH_WINDOWS.append((x + 200, y - 70, 120 + (x+200), 24 + (y-70)))

BOARD_POS_COORDS = []

for row in range(4):
    BOARD_POS_COORDS.append([])
    for col in range(7):
        if row == 0:
            x, y = 562, 410
            x += 114 * col
        elif row == 1:
            x, y = 610, 480
            x += 118 * col
        elif row == 2:
            x, y = 534, 560
            x += 123 * col
        else:
            x, y = 581, 670
            x += 128 * col
        BOARD_POS_COORDS[row].append((x, y))


def board_row_col(coordinate: tuple) -> tuple:
    row = -1
    col = -1
    if coordinate[1] == 410:
        row = 0
        x = 562
        for i in range(7):
            if x == coordinate[0]:
                col = i
                break
            x += 114
    elif coordinate[1] == 480:
        row = 1
        x = 610
        for i in range(7):
            if x == coordinate[0]:
                col = i
                break
            x += 118
    elif coordinate[1] == 560:
        row = 2
        x = 534
        for i in range(7):
            if x == coordinate[0]:
                col = i
                break
            x += 123
    elif coordinate[1] == 670:
        row = 3
        x = 581
        for i in range(7):
            if x == coordinate[0]:
                col = i
                break
            x += 128
    return row, col


UNIT_NAME_ON_BOARD_WINDOWS = []

for row in range(4):
    UNIT_NAME_ON_BOARD_WINDOWS.append([])
    for col in range(7):
        x, y = BOARD_POS_COORDS[row][col]
        UNIT_NAME_ON_BOARD_WINDOWS[row].append((x + 200, y - 70, 120 + x + 200, 24 + (y-70)))

ITEM_BENCH_COORDS = [
    (289, 753),
    (335, 721),
    (296, 687),
    (352, 673),
    (411, 673),
    (448, 631),
    (378, 627),
    (313, 631),
    (334, 586),
    (393, 586),
]

ITEM_NAME_WINDOWS = []

for (x, y) in ITEM_BENCH_COORDS:
    ITEM_NAME_WINDOWS.append((x + 100, y + 40, 170 + x + 100, 30 + y + 40))

