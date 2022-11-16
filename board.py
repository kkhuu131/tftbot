import Image
import comp
import game_stats
import game_info
import controller
import coordinates


class Unit:
    def __init__(self, name: str, coords: tuple, in_comp: bool, items: list) -> None:
        self.name = name
        self.coords = coords
        self.in_comp = in_comp
        self.items = items


# up to client to keep variables up to date with outside factors (ex. items from loot drops)
class Board:
    def __init__(self) -> None:
        self.level = 0
        self.bench: list[Unit and None] = [None, None, None, None, None, None, None, None, None]
        self.units: list[Unit] = []
        # list of units that we still need to buy
        self.units_to_buy: list[str] = []
        # list of unit names from our comp that we currently do not have fielded yet
        self.units_to_field: list[str] = []
        self.item_bench: list[str and None] = [None]*10

        # initialize
        for unit in comp.COMP:
            self.units_to_field.append(unit)
        for unit in comp.COMP:
            for i in range(3*comp.COMP[unit]["star"]):
                self.units_to_buy.append(unit)

    def buy_shop(self) -> None:
        shop = game_stats.get_shop()
        gold = game_stats.get_gold()

        for i in range(len(shop)):
            unit = shop[i]
            if unit in self.units_to_buy and game_info.unit_gold(unit) >= gold and None in self.bench:
                # buy unit
                controller.click(coordinates.SHOP_SLOT_COORDS[i])
                gold -= game_info.unit_gold(unit)
                self.units_to_buy.remove(unit)
                next_open_slot = self.next_open_bench_slot()
                bought_unit = Unit(unit,
                                   coordinates.BENCH_COORDS[next_open_slot],
                                   True,
                                   []
                                   )
                self.bench[next_open_slot] = bought_unit

    def next_open_bench_slot(self) -> int:
        for i in range(len(self.bench)):
            if not self.bench[i]:
                return i

        return -1

    def field_unit(self, bench_slot: int, row: int, col: int):
        """Benches a unit from col,row position on board to given slot from bench."""

        # bench slot is empty
        if not 0 <= bench_slot <= 8 or self.bench[bench_slot] not in game_info.CHAMPIONS:
            return
        bench_pos = coordinates.BENCH_COORDS[bench_slot]
        board_pos = coordinates.BOARD_POS_COORDS[row][col]

        controller.drag(bench_pos, board_pos)

        for board_unit in self.units:
            # there was a unit occupying the spot we moved to
            # board unit: unit originally on board
            # unit: unit originally on bench
            if board_pos == board_unit.coords:
                unit = self.bench[bench_slot]
                self.bench[bench_slot] = board_unit
                self.units.remove(board_unit)
                self.units.append(unit)

                # these lines could have interference if we how multiple of the same unit in the COMP
                if board_unit.name in comp.COMP and board_unit.name in self.units_to_field:
                    self.units_to_field.remove(board_unit.name)
                if unit.name in comp.COMP and unit.name not in self.units_to_field:
                    self.units_to_field.append(unit.name)
                return
            else:
                # spot was unoccupied
                unit = self.bench[bench_slot]
                self.bench[bench_slot] = None
                self.units.append(unit)
                if unit.name in comp.COMP and unit.name not in self.units_to_field:
                    self.units_to_field.append(unit.name)

    def bench_unit(self, bench_slot: int, row: int, col: int):
        """Benches a unit from col,row position on board to given slot from bench."""
        # board slot is empty
        bench_pos = coordinates.BENCH_COORDS[bench_slot]
        board_pos = coordinates.BOARD_POS_COORDS[row][col]
        board_unit = None
        for unit in self.units:
            if unit.coords == board_pos:
                board_unit = unit
        if not board_unit:
            return

        controller.drag(bench_pos, board_pos)

        # there was a unit occupying the bench slot
        if self.bench[bench_slot]:
            bench_unit = self.bench[bench_slot]
            self.bench[bench_slot] = board_unit
            self.units.remove(board_unit)
            self.units.append(bench_unit)
            if board_unit.name in comp.COMP and board_unit.name in self.units_to_field:
                self.units_to_field.remove(board_unit.name)
            if bench_unit.name in comp.COMP and bench_unit.name not in self.units_to_field:
                self.units_to_field.append(bench_unit.name)
        # spot was unoccupied
        else:
            self.units.remove(board_unit)
            self.bench[bench_slot] = board_unit
            if board_unit.name in comp.COMP and board_unit.name in self.units_to_field:
                self.units_to_field.remove(board_unit.name)

    def position_unit(self, row1: int, col1: int, row2: int, col2: int):
        """Moves a unit from col1,row1 position on board to col2,row2 position on board."""
        # board slot is empty
        board_pos_1 = coordinates.BOARD_POS_COORDS[row1][col1]
        board_pos_2 = coordinates.BOARD_POS_COORDS[row2][col2]
        board_unit_1 = None
        board_unit_2 = None
        for unit in self.units:
            if unit.coords == board_pos_1:
                board_unit_1 = unit
            if unit.coords == board_pos_2:
                board_unit_2 = unit
        if not board_unit_1:
            return

        controller.drag(board_pos_1, board_pos_2)

        # there was a unit occupying the other board slot
        if not board_unit_2:
            board_unit_1.coords = board_pos_2
            board_unit_2.coords = board_pos_1
        # spot was unoccupied
        else:
            board_unit_1.coords = board_pos_2

    def search_bench(self, unit: str) -> int:
        for i in range(len(self.bench)):
            if unit == self.bench[i]:
                return i
        return -1

    def clear_bench(self):
        """Sells unit on bench not pertaining to comp."""
        for i in range(len(self.bench)):
            unit_name = game_stats.get_bench_slot(i)
            if unit_name not in self.units_to_buy and unit_name not in self.units_to_field: # ?
                controller.move_mouse(coordinates.BENCH_COORDS[i])
                controller.sell()
                self.bench[i] = None

    def set_up_board(self):
        """Sets up the board by fielding and filling in board slots and replacing units on board."""
        self.level = game_stats.get_level()
        self.update_bench()

        # First, put in priority units
        for i in range(len(self.bench)):
            unit_name: str = self.bench[i].name
            # if it is a unit in our comp that we haven't fielded yet
            if unit_name in self.units_to_field:
                row, col = comp.COMP[unit_name]["position"][0], comp.COMP[unit_name]["position"][1]
                # if there is space
                if len(self.units) < self.level or self.unit_at_board_position(row, col):
                    self.field_unit(i, row, col)
                else:
                    # see if there are non-comp units on board to replace
                    for unit in self.units:
                        if unit.name not in comp.COMP:
                            sell_row, sell_col = coordinates.board_row_col(unit.coords)
                            self.sell_board_unit(sell_row, sell_col)
                            self.field_unit(i, row, col)
                            break

        # Then, if there is still remaining space, put in extras
        shop: list[str] = game_stats.get_shop()
        remaining_space: int = self.level - len(self.units)

        # list of row, col to put placeholder units
        spots_to_fill = []
        for unit in self.units_to_field:
            row, col = comp.COMP[unit]["position"]
            if not self.unit_at_board_position(row, col):
                spots_to_fill.append(comp.COMP[unit]["position"])

        for i in range(remaining_space):
            # check if any non-comp units already on bench to field
            filled = False
            for j in range(len(self.bench)):
                unit_name: str = self.bench[j].name

                if unit_name not in comp.COMP:
                    row, col = spots_to_fill.pop()
                    self.field_unit(j, row, col)
                    filled = True
                    break
            # no non-comp units on bench, so buy a unit from shop and field it
            if not filled:
                for j in range(len(shop)):
                    if shop[j] != "" and shop[j] not in comp.COMP: # ?
                        self.buy_shop_slot(j)
                        for k in range(len(self.bench)):
                            unit_name: str = self.bench[k].name
                            if unit_name not in comp.COMP:
                                row, col = spots_to_fill.pop()
                                self.field_unit(j, row, col)
                                break
                        break

    def buy_shop_slot(self, slot: int) -> bool:
        shop = game_stats.get_shop()
        open_slot = self.next_open_bench_slot()
        gold = game_stats.get_gold()
        if shop[slot] in game_info.CHAMPIONS and \
                game_info.unit_gold(shop[slot]) <= gold and \
                open_slot != -1:
            controller.click(coordinates.SHOP_SLOT_COORDS[slot])
            self.bench[open_slot] = Unit(shop[slot], coordinates.BENCH_COORDS[open_slot], shop[slot] in comp.COMP, [])
            return True
        else:
            return False

    def sell_board_unit(self, row: int, col: int) -> None:
        unit = self.unit_at_board_position(row, col)
        if unit:
            coord = coordinates.BOARD_POS_COORDS[row][col]
            controller.move_mouse(coord)
            controller.sell()
            self.units.remove(unit)
            if unit.name in comp.COMP and unit.name in self.units_to_field:
                self.units_to_field.remove(unit.name)

    def unit_at_board_position(self, row, col) -> Unit or None:
        for i in range(len(self.units)):
            if coordinates.BOARD_POS_COORDS[row][col] == self.units[i].coords:
                return self.units[i]
        return None

    def update_bench(self):
        """Keep bench up to date"""

        for i in range(len(self.bench)):
            unit_name = game_stats.get_bench_slot(i)
            if unit_name == "":
                self.bench[i] = None
            elif unit_name in game_info.CHAMPIONS:
                in_comp = unit_name in comp.COMP
                self.bench[i] = Unit(unit_name, coordinates.BENCH_COORDS[i], in_comp, [])

    def put_item(self, item_index: int, unit_index: int):
        """Puts an item from bench onto a unit on board"""
        def has_a_component(u: Unit) -> int:
            for i in range(len(u.items)):
                if u.items[i] in game_info.COMPONENTS:
                    return i
            return -1

        unit = self.units[unit_index]
        item_is_component: bool = self.item_bench[item_index in game_info.COMPONENTS]
        # if valid item and unit has item space left
        if self.item_bench[item_index] in game_info.ITEMS and \
                (len(unit.items) < 3 or (has_a_component(unit) != -1 and item_is_component)):
            controller.drag(coordinates.ITEM_BENCH_COORDS[item_index], unit.coords)
            # if both are components
            if len(unit.items) > 0 and has_a_component(unit) != -1 and item_is_component:
                old_component_index = has_a_component(unit)
                components = (unit.items[old_component_index], self.item_bench[item_index])
                full_item = game_info.COMPONENTS_TO_ITEM(components)
                unit.items[old_component_index] = full_item
            else:
                unit.items.append(self.item_bench[item_index])

            self.item_bench[item_index] = None

    def slam_items(self):
        for i in range(len(self.units)):
            unit = self.units[i]
            if unit.name in comp.COMP:
                items = comp.COMP[unit]["items"]
                for item in items:
                    if item not in unit.items:
                        i1, i2 = self.can_make_item(item)
                        if i1 != -1 and i2 != -1:
                            self.put_item(i1, i)
                            self.put_item(i2, i)

    def can_make_item(self, item: str) -> (int, int):
        i1 = -1
        i2 = -1
        component1, component2 = game_info.ITEM_TO_COMPONENTS(item)
        for i in range(len(self.item_bench)):
            if self.item_bench[i] == component1:
                i1 = i
                break

        for i in range(len(self.item_bench)):
            if self.item_bench[i] == component2 and i != i1:
                i2 = i
                break

        if i1 != -1 and i2 != -1:
            return i1, i2
        else:
            return -1, -1

    def carousel(self):
        # Determine items we need
        needed_items = []
        for unit in comp.COMP:
            items = comp.COMP[unit]["items"]
            if unit in self.units:
                board_unit = self.units[self.units.index(unit)]
                for unit_item in board_unit.items:
                    if unit_item in items:
                        items.remove(unit_item)

            for item in items:
                needed_items.append(item)

        for item in self.item_bench:
            if item in needed_items:
                needed_items.remove(item)

        needed_components = {}
        for item in needed_items:
            component1, component2 = game_info.ITEM_TO_COMPONENTS(item)
            if component1 not in needed_components:
                needed_components[component1] = 0
            if component2 not in needed_components:
                needed_components[component2] = 0
            needed_components[component1] -= 1
            needed_components[component2] -= 1

        for item in self.item_bench:
            if item in needed_components:
                needed_components[item] += 1

        import numpy as np
        sorted_value_index = np.argsort(needed_components.values())
        dictionary_keys = list(needed_components.keys())
        sorted_dict = {dictionary_keys[i]: sorted(
            needed_components.values())[i] for i in range(len(dictionary_keys))}

        from PIL import Image as PILImage
        from PIL import ImageDraw as PILImageDraw

        found = True
        while found:
            found = False
            for item in sorted_dict:
                item_img = Image.get_item_img(item)
                carousel_window = (707, 246, 707+480, 246+360)
                image = Image.get_screen(carousel_window)
                lum_img = PILImage.new('L', (480, 360), 0)
                draw = PILImageDraw.Draw(lum_img)
                draw.pieslice(((0, 0), (480, 360)), 0, 360, fill=255)
                image_array = Image.image_array(image)
                lum_img_array = Image.image_array(lum_img)
                final_img_array = np.dstack((image_array, lum_img_array))
                modified_image = PILImage.fromarray(final_img_array)

                x, y = Image.find_image_on_image(item_img, 0.15, modified_image)

                if x != -1 and y != -1:
                    found = True
                    x += 707
                    y += 246
                    center_x, center_y = 947, 700
                    diff_x, diff_y = x - center_x, y - center_y
                    diff_x, diff_y = diff_x * 0.8, diff_y * 0.8
                    controller.click((int(center_x + diff_x), int(center_y + diff_y)))
                    break


def collect_items():
    gray_drop_img = Image.get_drop_img('Gray')
    blue_drop_img = Image.get_drop_img('Blue')
    gold_drop_img = Image.get_drop_img('Gold')

    gray_location = Image.find_image_on_screen(gray_drop_img, 0.15, coordinates.SCREEN_WINDOW)
    blue_location = Image.find_image_on_screen(blue_drop_img, 0.15, coordinates.SCREEN_WINDOW)
    gold_location = Image.find_image_on_screen(gold_drop_img, 0.15, coordinates.SCREEN_WINDOW)
    invalid_location = (-1, -1)
    while gray_location != invalid_location and blue_location != invalid_location and gold_location != invalid_location:
        if gray_location != invalid_location:
            controller.move(gray_location)
        elif blue_location != invalid_location:
            controller.move(gray_location)
        elif gray_location != invalid_location:
            controller.move(gray_location)


def lock_shop():
    """Locks the shop. Unlocks if shop is already locked."""
    controller.click((1452, 901))


def decide_augment() -> str:
    augments = game_stats.get_augments()
    # 0: good, 1: neutral, 2: bad
    priority = [1]*len(augments)
    for i in range(len(augments)):
        if augments[i] in comp.TARGET_AUGMENTS:
            priority[i] = 0
        elif augments[i] in comp.AVOID_AUGMENTS:
            priority[i] = 2

    # get best augment
    best_priority = 3
    index = -1

    for i in range(len(priority)):
        if priority[i] < best_priority:
            best_priority = priority[i]
            index = i

    # reroll augments
    if best_priority == 2:
        return decide_augment()

    controller.click(coordinates.AUGMENT_COORDS[index])
    return augments[index]





