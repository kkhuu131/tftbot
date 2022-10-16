import win32api

import TFTapi
import time
from waiting import wait
import curses


# Curses set up (dynamic terminal)
stdscr = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)


# COMP VARIABLES

target_units = ['nidalee', 'skarn', 'viad', 'lux', 'varus', 'sylas']
# [column, row]
unit_positions = [[1, 1], [2, 0], [3, 0], [0, 3], [1, 3], [4, 0]]
# set ideal amount of each unit
target_amount = [9, 9, 9, 9, 3, 3, 3]
# set ideal augments (order matters) and unplayable augments
target_augments = ["Weakspot", "Feather", "Thrill", "Celestial"]
avoid_augments = ["Soul", "Heart", "Crest", "Built Different", "Double", "Big", "Lategame", "Luden",
                  "Exile", "Recombobulator", "Tri", "Stand", "Mind", "Axiom", "Ancient", "Den", "Friend", "Dragon",
                  "Gear", "Future", "Heroic", "Hot", "Hustler", "Hallucinate", "Mage",
                  "Gifts", "Loot", "Party", "Penitence", "Inspire", "Storm", "Eternal", "Ricochet",
                  "Titanic", "Tiamat", "Trade", "Binary", "Cavalier", "Cursed", "Cruel", "Think", "Phony", "Forge",
                  "Radiant", "Essence"]

# set ideal items (one is the total set of components, other is formatted as full items)
# i, j, k
# i refers to which unit
# j refers to which item slot (3 for each unit)
# k refers to option(s) for that item slot (items and its alternatives basically)
# l refers to the components of each item
target_items = [
                [[["bow", "vest"], ["bow", "rod"]], [["glove", "tear"], ["sword", "cloak"]], [[["sword", "glove"]]]],

                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                []
                ]

# NOT FOR USE
target_components = []

for unit in target_items:
    for item_slot in unit:
        for item in item_slot:
            for component in item:
                target_components.append(component)

unitemized_units = []
for unit in target_items:
    unitemized_units.append(not unit)


# STATE VARIABLES (NOT FOR USE)

gold = 0
stage = 10
level = 0
fielded_units = []
number_fielded = 0
filled_units = []
number_filled = 0

for i in range(len(target_units)):
    fielded_units.append(False)
    filled_units.append(False)


items = []
augment_reroll_left = True
augments = []


# GUI variables and functions
# root = tk.Tk()

# gold_text = tk.StringVar()
# gold_text.set("Gold: " + str(gold))
# gold_label = tk.Label(root, textvariable=gold_text)
# gold_label.pack()

# stage_text = tk.StringVar()
# stage_text.set("Stage: " + str(stage%10) + "-" + str(stage/10))
# stage_label = tk.Label(root, textvariable=stage_text)
# stage_label.pack()


# SCRIPT FUNCTIONS

def wait_until_next_stage():
    """Pauses program until next stage is reached. Does not work for stage 1."""
    global stage
    read_stage = TFTapi.stage()
    if read_stage == stage+1 or (read_stage % 10 == 1 and int(read_stage/10) == int(stage/10) + 1):
        stage = read_stage
        time.sleep(1.5)
        return True
    else:
        return False


def wait_until_next_early_stage():
    """Pauses program until next stage is reached. Only works for stage 1"""
    global stage
    read_stage = TFTapi.early_stage()
    if read_stage == stage+1 or (read_stage % 10 == 1 and int(read_stage/10) == int(stage/10) + 1):
        stage = read_stage
        time.sleep(1.5)
        return True
    else:
        return False


def slam_items():
    """Combines any items that we can make on to the according unit. Then slams unneeded components randomly."""

    global items
    items = TFTapi.items()

    priority_components = []

    # slam any full items we need and have
    for unit_index in range(len(target_items)):
        unit_items = target_items[unit_index]
        priority_unit_components = []
        for item_slot in range(len(unit_items)):
            for item in unit_items[item_slot]:
                if item[0] not in priority_components and item[1] not in priority_components:
                    i, j = have_full_item(item[0], item[1], items)
                    if i != -1 and fielded_units[0]:
                        items1x, items1y = TFTapi.get_items_pos(i)
                        items2x, items2y = TFTapi.get_items_pos(j)
                        unitx, unity = TFTapi.get_board_pos(unit_positions[unit_index][0], unit_positions[unit_index][1])
                        TFTapi.drag(items1x, items1y, unitx, unity)
                        time.sleep(0.5)
                        TFTapi.drag(items2x, items2y, unitx, unity)
                        target_items[unit_index].remove(item_slot)
                        items[i] = ""
                        items[j] = ""
                        break
                    else:
                        # makes sure we don't use any components that we need for higher priority units
                        # (doesn't include components from alternative items options)
                        # might need to change logic to be more flexible
                        if item_slot == 0:
                            priority_unit_components.append(item[0])
                            priority_unit_components.append(item[1])
        for component in priority_unit_components:
            priority_components.append(component)

    # slam remaining unneeded components on other units
    for i in range(len(items)):
        if not any(substring.lower() in items[i].lower() for substring in target_components):
            if "remover" not in items[i].lower() and "champion" not in items[i].lower() and "reforger" \
                    not in items[i].lower() and items[i] != '':
                unit_index = -1
                for n in range(len(fielded_units)-1, 0, -1):
                    if fielded_units[n] and unitemized_units[n]:
                        unit_index = n
                        break
                if unit_index != -1:
                    itemsx, itemsy = TFTapi.get_items_pos(i)
                    x, y = TFTapi.get_board_pos(unit_positions[unit_index][0], unit_positions[unit_index][1])
                    TFTapi.drag(itemsx, itemsy, x, y)
                    items[i] = ""


def have_full_item(c1, c2, items):
    """Checks if we have both components. Returns associated indexes, otherwise -1 if we don't."""
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] != '' and items[j] != '':
                if (c1.lower() in items[i].lower() and c2.lower() in items[j].lower()) or \
                        (c1.lower() in items[j].lower() and c2.lower() in items[i].lower()):
                    return i, j
    return -1, -1


def decide_augment():
    """Based on our priority augments and augments we want to avoid, selects the best augment possible."""
    augment = ""
    augments = TFTapi.read_augments()
    priority_order = [len(target_augments), len(target_augments), len(target_augments)]

    # calculate priorities of augments based on desired and avoided info
    for i in range(len(augments)):
        for j in range(len(avoid_augments)):
            if j < len(target_augments) and target_augments[j].lower() in augments[i].lower():
                priority_order[i] = j
                break
            if avoid_augments[j].lower() in augments[i].lower():
                priority_order[i] = len(target_augments)+1
                break

    highest_priority = min(priority_order)
    global augment_reroll_left
    # if all should be avoided
    if highest_priority == len(target_augments)+1 and augment_reroll_left:
        TFTapi.reroll_augment()
        augment_reroll_left = False
        augment = decide_augment()
    else:
        # decide
        index = priority_order.index(highest_priority)
        TFTapi.pick_augment(index)
        augment = augments[index]
    return augment


def set_up_board():
    """Sets up the board by fielding and filling in board slots and replacing units on board."""
    global level
    level = TFTapi.level()
    global number_fielded
    global number_filled
    bench = TFTapi.bench()

    for i in range(len(fielded_units)):
        bench_index = TFTapi.search_bench(bench, target_units[i])
        # do we have the priority unit in our bench and its not on our board yet
        if bench_index != -1 and not fielded_units[i]:
            # if dragon unit, go to special case (since they take up 2 slots)
            if i == 2:
                add_in_dragon(level, i, bench)
            # replace associated filler unit with its actual unit
            elif filled_units[i]:
                col, row = unit_positions[i][0], unit_positions[i][1]
                TFTapi.unbench_unit(bench, target_units[i], col, row)
                fielded_units[i] = True
                number_fielded = number_fielded + 1
                filled_units[i] = False
                number_filled = number_filled - 1
            # just add in if there's open space
            elif number_fielded + number_filled < level:
                col, row = unit_positions[i][0], unit_positions[i][1]
                TFTapi.unbench_unit(bench, target_units[i], col, row)
                fielded_units[i] = True
                number_fielded = number_fielded + 1
            # replace another filler unit that has lower priority (target_units priority goes from left to right)
            elif True in filled_units and 0 <= filled_units.index(True) < i:
                replace_index = filled_units.index(True)
                x, y = TFTapi.get_board_pos(unit_positions[replace_index][0], unit_positions[replace_index][1])
                win32api.SetCursorPos((x, y))
                TFTapi.sell()
                x1, y1 = TFTapi.get_bench_pos(bench_index)
                x2, y2 = TFTapi.get_board_pos(unit_positions[i][0], unit_positions[i][1])
                TFTapi.drag(x1, y1, x2, y2)
                bench[bench_index] = ""
                filled_units[replace_index] = False
                number_filled = number_filled - 1
                fielded_units[i] = True
                number_fielded = number_fielded + 1
            # replace a fielded unit that has lower priority
            elif True in fielded_units and fielded_units.index(True) < i:
                replace_index = fielded_units.index(True)
                x1, y1 = TFTapi.get_bench_pos(bench_index)
                x2, y2 = TFTapi.get_board_pos(unit_positions[replace_index][0], unit_positions[replace_index][1])
                x3, y3 = TFTapi.get_board_pos(unit_positions[i][0], unit_positions[i][1])
                TFTapi.drag(x1, y1, x2, y2)
                TFTapi.drag(x2, y2, x3, y3)
                bench[bench_index] = target_units[replace_index]
                fielded_units[i] = True
                fielded_units[replace_index] = False
    return bench


def add_in_dragon(level, i, bench):
    """Adds in a dragon unit (that takes 2 slots). NOT TESTED."""
    global number_fielded
    global number_filled
    space_available = 0
    if number_fielded+number_filled < level:
        space_available = space_available + 1
    if filled_units[i]:
        space_available = space_available + 1
    if True in filled_units and 0 <= filled_units.index(True) < i and space_available < 2:
        space_available = space_available + 1
    if True in fielded_units and fielded_units.index(True) < i and "" in bench and space_available < 2:
        space_available = space_available + 1

    if space_available >= 2:
        space_made = 0
        if number_fielded+number_filled < level and space_made < 2:
            space_made = space_made + 1
        if filled_units[i] and space_made < 2:
            filled_units[i] = False
            number_filled = number_filled - 1
            win32api.SetCursorPos((unit_positions[i][0], unit_positions[i][1]))
            space_made = space_made + 1
        if True in filled_units and 0 <= filled_units.index(True) < i and space_made < 2:
            replace_index = filled_units.index(True)
            x, y = TFTapi.get_board_pos(unit_positions[replace_index][0], unit_positions[replace_index][1])
            win32api.SetCursorPos((x, y))
            TFTapi.sell()
            filled_units[replace_index] = False
            number_filled = number_filled - 1
            fielded_units[i] = True
            number_fielded = number_fielded + 1
            space_made = space_made + 1
        if True in fielded_units and fielded_units.index(True) < i and "" in bench and space_made < 2:
            replace_index = fielded_units.index(True)
            next_clear_bench_slot = bench.index("")
            x1, y1 = TFTapi.get_board_pos(unit_positions[replace_index][0], unit_positions[replace_index][1])
            x2, y2 = TFTapi.get_bench_pos(next_clear_bench_slot)
            TFTapi.drag(x1, y1, x2, y2)
            bench[next_clear_bench_slot] = target_units[replace_index]
            fielded_units[replace_index] = False
            space_made = space_made + 1
        TFTapi.unbench_unit(bench, target_units[i], unit_positions[i][0], unit_positions[i][1])
        fielded_units[i] = True
        number_fielded = number_fielded + 2
        return True
    else:
        return False


# fill board with units from shop
def fill_board(shop_slots, bench_slots):
    """Places in filler units for board positions if the position isn't occupied by a target unit."""
    global number_filled
    global number_fielded
    num_units = number_fielded + number_filled

    current_level = TFTapi.level()
    for i in range(current_level-num_units):
        bench_index = bench_slots.index("")
        slot = -1
        for n in range(len(shop_slots)):
            if shop_slots[n] != -1 and shop_slots[n] < 6:
                slot = n
                break
        TFTapi.buy_slot(slot)
        shop_slots[slot] = -1
        fill_in_index = -1
        for i in range(len(filled_units)):
            if not filled_units[i] and not fielded_units[i]:
                fill_in_index = i
                break
        filled_units[fill_in_index] = True
        col, row = unit_positions[fill_in_index]
        TFTapi.field_unit(bench_index, col, row)
        number_filled = number_filled + 1


def display_state():
    """Displays current stats of game using a dynamic text terminal."""
    stdscr.clear()

    stdscr.addstr("Comp: ", curses.color_pair(1))
    for i in range(len(target_units)):
        if fielded_units[i]:
            stdscr.addstr(str(target_units[i]), curses.color_pair(2))
        elif filled_units[i]:
            stdscr.addstr(str(target_units[i]), curses.color_pair(3))
        else:
            stdscr.addstr(str(target_units[i]), curses.color_pair(4))

        if i == len(target_units)-1:
            stdscr.addstr("\n")
        else:
            stdscr.addstr(", ")

    stdscr.addstr("Stage: ", curses.color_pair(1))
    stdscr.addstr(str(int(stage/10)) + "-" + str(int(stage % 10)) + "\n")
    stdscr.addstr("Gold: ", curses.color_pair(1))
    stdscr.addstr(str(gold) + "\n")
    stdscr.addstr("Items: ", curses.color_pair(1))
    stdscr.addstr(str(items) + "\n")
    stdscr.addstr("Augments: ", curses.color_pair(1))
    stdscr.addstr(str(augments) + "\n")
    stdscr.addstr("\n")
    display_board()

    stdscr.refresh()


def display_board():
    """Dynamically displays the current board of the game on the terminal."""

    global target_units, unit_positions, fielded_units, filled_units

    stdscr.addstr('    0  1  2  3  4  5  6 \n')

    # for each row
    for i in range(0, 4):
        if i % 2 == 0:
            stdscr.addstr(str(i) + "  ")
        else:
            stdscr.addstr(str(i) + "   ")
        # for each column
        for j in range(0, 7):
            stdscr.addstr("[")
            if [j, i] in unit_positions:
                index = unit_positions.index([j, i])
                if fielded_units[index]:
                    stdscr.addstr((target_units[index][0]).upper(), curses.color_pair(2))
                elif filled_units[index]:
                    stdscr.addstr("#", curses.color_pair(3))
                else:
                    stdscr.addstr("X", curses.color_pair(4))
            else:
                stdscr.addstr(" ")
            stdscr.addstr("]")

        stdscr.addstr("\n")


# START
stdscr.clear()
stdscr.addstr("████████╗███████╗████████╗██████╗  ██████╗ ████████╗\n")
stdscr.addstr("╚══██╔══╝██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗╚══██╔══╝\n")
stdscr.addstr("   ██║   █████╗     ██║   ██████╔╝██║   ██║   ██║   \n")
stdscr.addstr("   ██║   ██╔══╝     ██║   ██╔══██╗██║   ██║   ██║   \n")
stdscr.addstr("   ██║   ██║        ██║   ██████╔╝╚██████╔╝   ██║   \n")
stdscr.addstr("   ╚═╝   ╚═╝        ╚═╝   ╚═════╝  ╚═════╝    ╚═╝   \n")
stdscr.addstr("Queue up to start...\n")
stdscr.refresh()

TFTapi.accept_queue()

# augments occur at stage 2-1, 3-2, 5-1
# creeps occur at stage 1-2, 1-3, 1-4, 2-7, 3-7, 4-7 (dragon treasure), 5-7, 6-7, 7-7
# carousels occur at stage 1-1, 2-4, 3-4, 4-4, 5-4, 6-4, 7-4


# STAGE 1
wait(lambda: TFTapi.wait_until_game_start(), timeout_seconds=60, waiting_for="1-1")
time.sleep(6)
TFTapi.carousel(target_components, 11)
stage = 11
display_state()

wait(lambda: wait_until_next_early_stage(), timeout_seconds=60, waiting_for="1-2")
TFTapi.field_unit(0, 0, 0)
TFTapi.collect_items(6, True)
display_state()

wait(lambda: wait_until_next_early_stage(), timeout_seconds=60, waiting_for="1-3")
x, y = TFTapi.get_board_pos(0,0)
win32api.SetCursorPos((x,y))
TFTapi.sell()
fill_board(TFTapi.buy_out_units(target_units, target_amount), set_up_board())
TFTapi.collect_items(10, False)
TFTapi.clear_bench(target_units, target_amount)
display_state()

wait(lambda: wait_until_next_early_stage(), timeout_seconds=60, waiting_for="1-4")
fill_board(TFTapi.buy_out_units(target_units, target_amount), set_up_board())
TFTapi.clear_bench(target_units, target_amount)
display_state()

wait(lambda: wait_until_next_stage(), timeout_seconds=60, waiting_for="2-1")
augments.append(decide_augment())
time.sleep(2)
fill_board(TFTapi.buy_out_units(target_units, target_amount), set_up_board())
TFTapi.collect_items(5, False)
TFTapi.clear_bench(target_units, target_amount)
slam_items()
display_state()

wait(lambda: wait_until_next_stage(), timeout_seconds=60, waiting_for="2-2")
fill_board(TFTapi.buy_out_units(target_units, target_amount), set_up_board())
TFTapi.clear_bench(target_units, target_amount)
display_state()

wait(lambda: wait_until_next_stage(), timeout_seconds=60, waiting_for="2-3")
fill_board(TFTapi.buy_out_units(target_units, target_amount), set_up_board())
carousel_unit_slot = TFTapi.clear_bench(target_units, target_amount)
display_state()

wait(lambda: wait_until_next_stage(), timeout_seconds=60, waiting_for="2-4")
TFTapi.carousel(target_components, 24)
display_state()

wait(lambda: wait_until_next_stage(), timeout_seconds=60, waiting_for="2-5")
x, y = TFTapi.get_bench_pos(carousel_unit_slot)
win32api.SetCursorPos((x, y))
TFTapi.sell()
fill_board(TFTapi.buy_out_units(target_units, target_amount), set_up_board())
TFTapi.clear_bench(target_units, target_amount)
display_state()

wait(lambda: wait_until_next_stage(), timeout_seconds=60, waiting_for="2-6")
fill_board(TFTapi.buy_out_units(target_units, target_amount), set_up_board())
TFTapi.clear_bench(target_units, target_amount)
display_state()

wait(lambda: wait_until_next_stage(), timeout_seconds=60, waiting_for="2-7")
fill_board(TFTapi.buy_out_units(target_units, target_amount), set_up_board())
TFTapi.clear_bench(target_units, target_amount)
TFTapi.collect_items(25, True)
display_state()
