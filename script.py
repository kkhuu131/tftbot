import win32api

import TFTapi
import time
from waiting import wait


# COMP VARIABLES

# order specifies priority
target_units = ['sett', 'senna', 'shyvana', 'shen', 'hecarim', 'swain', 'xayah', 'kayn']
# col, then row
unit_positions = [[0, 0], [0, 3], [3, 0], [1, 0], [2, 0], [1, 3], [2, 3], [3, 1]]
# set ideal amount of each unit
target_amount = [9, 3, 3, 3, 3, 3, 3, 3]
# set ideal augments (order matters) and unplayable augments
target_augments = ["Scorch", "Tantrum", "Weakspot", "Thrill", "Celestial", "Feather", "Ascension"]
avoid_augments = ["Soul", "Heart", "Crest", "Built Different", "Double", "Big", "Lategame", "Luden",
                  "Exile", "Recombobulator", "Tri", "Stand", "Mind", "Axiom", "Ancient", "Den", "Friend", "Dragon",
                  "Gear", "Future", "Heroic", "Hot", "Hustler", "Hallucinate", "Mage",
                  "Gifts", "Loot", "Party", "Penitence", "Inspire", "Storm", "Eternal", "Ricochet",
                  "Titanic", "Tiamat", "Trade", "Binary", "Cavalier", "Cursed", "Cruel", "Think", "Phony", "Forge",
                  "Radiant", "Essence"]
# set ideal items (one is the total set of components, other is formatted as full items)
# as of now, these items are only for the highest priority unit
target_items = ["bow", "needless", "glove", "cloak", "sword", "bow"]
needed_items = [["bow", "needless"], ["glove", "cloak"], ["sword", "bow"]]

# STATE VARIABLES

gold = 0
stage = 10
level = 0
fielded_units = [False, False, False, False, False, False, False, False]
number_fielded = 0
filled_units = [False, False, False, False, False, False, False, False]
number_filled = 0

items = []
augment_reroll_left = True


# SCRIPT FUNCTIONS


def wait_until_next_stage():
    global stage
    read_stage = TFTapi.stage()
    if read_stage == stage+1 or (read_stage % 10 == 1 and int(read_stage/10) == int(stage/10) + 1):
        stage = read_stage
        print("Stage " + str(int(stage/10)) + "-" + str(int(stage % 10)))
        time.sleep(1.5)
        return True
    else:
        return False


def wait_until_next_early_stage():
    global stage
    read_stage = TFTapi.early_stage()
    if read_stage == stage+1 or (read_stage % 10 == 1 and int(read_stage/10) == int(stage/10) + 1):
        stage = read_stage
        print("Stage " + str(int(stage/10)) + "-" + str(int(stage % 10)))
        time.sleep(1.5)
        return True
    else:
        return False


def have_components(c1, c2):
    have1 = -1
    have2 = -1
    for i in range(len(items)):
        if c1 in items[i]:
            have1 = i

    for i in range(len(items)):
        if i != have1 and c2 in items[i]:
            have2 = i

    return have1, have2


def slam_items():
    global items
    items = TFTapi.items()
    print(items)

    for item in needed_items:
        i, j = have_full_item(item[0], item[1], items)
        if i != -1 and fielded_units[0]:
            print("MAKING ITEM on sett: " + item[0], item[1])
            print(i)
            print(items[i])
            print(j)
            print(items[j])
            items1x, items1y = TFTapi.get_items_pos(i)
            items2x, items2y = TFTapi.get_items_pos(j)
            unitx, unity = TFTapi.get_board_pos(unit_positions[0][0], unit_positions[0][1])
            TFTapi.drag(items1x, items1y, unitx, unity)
            time.sleep(0.5)
            TFTapi.drag(items2x, items2y, unitx, unity)
            needed_items.remove(item)
            items[i] = ""
            items[j] = ""

    for i in range(len(items)):
        if not any(substring.lower() in items[i].lower() for substring in target_items):
            if "remover" not in items[i].lower() and "champion" not in items[i].lower() and "reforger" \
                    not in items[i].lower() and items[i] != '':
                unit_index = -1
                for n in range(len(fielded_units)-1, 0, -1):
                    if fielded_units[n]:
                        unit_index = n
                        break
                if unit_index != -1:
                    print("slamming " + items[i].lower() + target_units[unit_index])
                    itemsx, itemsy = TFTapi.get_items_pos(i)
                    x, y = TFTapi.get_board_pos(unit_positions[unit_index][0], unit_positions[unit_index][1])
                    TFTapi.drag(itemsx, itemsy, x, y)
                    items[i] = ""


def have_full_item(c1, c2, items):
    for i in range(len(items)):
        for j in range(len(items)):
            if i != j and items[i] != '' and items[j] != '':
                if (c1.lower() in items[i].lower() and c2.lower() in items[j].lower()) or \
                        (c1.lower() in items[j].lower() and c2.lower() in items[i].lower()):
                    return i, j
    return -1, -1


def decide_augment():
    augments = TFTapi.read_augments()
    priority_order = [len(target_augments), len(target_augments), len(target_augments)]
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
    if highest_priority == len(target_augments)+1 and augment_reroll_left:
        TFTapi.reroll_augment()
        augment_reroll_left = False
        decide_augment()
    else:
        TFTapi.pick_augment(priority_order.index(highest_priority))


def set_up_board():
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
    print("fielded units:")
    print(fielded_units)
    print(number_fielded)
    return bench


def add_in_dragon(level, i, bench):
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
    global number_filled
    global number_fielded
    num_units = number_fielded + number_filled

    current_level = TFTapi.level()
    for i in range(current_level-num_units):
        bench_index = bench_slots.index("")
        slot = shop_slots.index(False)
        TFTapi.buy_slot(slot)
        shop_slots[slot] = True
        fill_in_index = -1
        for i in range(len(filled_units)):
            if not filled_units[i] and not fielded_units[i]:
                fill_in_index = i
                break
        filled_units[fill_in_index] = True
        col, row = unit_positions[fill_in_index]
        TFTapi.field_unit(bench_index, col, row)
        number_filled = number_filled + 1
        time.sleep(0.1)
    print("filled units:")
    print(filled_units)
    print(number_filled)


print("████████╗███████╗████████╗██████╗  ██████╗ ████████╗")
print("╚══██╔══╝██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗╚══██╔══╝")
print("   ██║   █████╗     ██║   ██████╔╝██║   ██║   ██║   ")
print("   ██║   ██╔══╝     ██║   ██╔══██╗██║   ██║   ██║   ")
print("   ██║   ██║        ██║   ██████╔╝╚██████╔╝   ██║   ")
print("   ╚═╝   ╚═╝        ╚═╝   ╚═════╝  ╚═════╝    ╚═╝   ")
print()
print("Queue up to start...")

# TFTapi.accept_queue()
print("Starting game")

# augments occur at stage 2-1, 3-5, 5-1
# creeps occur at stage 1-2, 1-3, 1-4, 2-7, 3-7, 4-7 (dragon treasure), 5-7, 6-7, 7-7
# carousels occur at stage 1-1, 2-4, 3-4, 4-4, 5-4, 6-4, 7-4

# STAGE 1
time.sleep(2)
TFTapi.carousel(target_items, 11)
stage = 11

wait(lambda: wait_until_next_early_stage(), timeout_seconds=60, waiting_for="1-2")
TFTapi.field_unit(0, 0, 0)
TFTapi.collect_items(6, True)
wait(lambda: wait_until_next_early_stage(), timeout_seconds=60, waiting_for="1-3")
x, y = TFTapi.get_board_pos(0,0)
win32api.SetCursorPos((x,y))
TFTapi.sell()
fill_board(TFTapi.buy_out_units(target_units, target_amount), set_up_board())
TFTapi.collect_items(10, False)
TFTapi.clear_bench(target_units, target_amount)

wait(lambda: wait_until_next_early_stage(), timeout_seconds=60, waiting_for="1-4")
fill_board(TFTapi.buy_out_units(target_units, target_amount), set_up_board())
TFTapi.clear_bench(target_units, target_amount)

wait(lambda: wait_until_next_stage(), timeout_seconds=60, waiting_for="2-1")
decide_augment()
time.sleep(2)
fill_board(TFTapi.buy_out_units(target_units, target_amount), set_up_board())
TFTapi.collect_items(5, False)
TFTapi.clear_bench(target_units, target_amount)
slam_items()

