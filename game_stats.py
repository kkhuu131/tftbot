import Image
import coordinates
import game_info
import controller
import time


def get_gold() -> int:
    """Reads the screen to determine the current amount of gold and returns it."""
    text = Image.get_screen_text(coordinates.GOLD_WINDOW, whitelist=Image.NUMBER_WHITELIST)

    if text.isdigit():
        return int(text)
    else:
        return -1


def get_stage() -> str:
    """Reads the screen to determine the current stage and returns it."""
    text = Image.get_screen_text(coordinates.STAGE_WINDOW, whitelist=Image.NUMBER_WHITELIST)

    if text in game_info.STAGES:
        return text

    text = Image.get_screen_text(coordinates.STAGE1_WINDOW, whitelist=Image.NUMBER_WHITELIST)

    if text in game_info.STAGES:
        return text

    return "0-0"


def get_level() -> int:
    text = Image.get_screen_text(coordinates.LEVEL_WINDOW, whitelist=Image.NUMBER_WHITELIST)

    if text.isdigit():
        return int(text)
    else:
        return -1


def get_augments() -> list[str]:
    augments: list[str] = []

    for i in range(3):
        text = Image.get_screen_text(coordinates.AUGMENT_NAME_WINDOWS[i], whitelist=Image.ALPHABET_WHITELIST)
        augments.append(text)

    return augments


def get_items() -> list[str]:
    items: list[str] = []

    for i in range(10):
        controller.move_mouse(coordinates.ITEM_BENCH_COORDS[i])
        text = Image.get_screen_text(coordinates.ITEM_NAME_WINDOWS[i], whitelist=Image.ALPHABET_WHITELIST)
        if text in game_info.ITEMS:
            items.append(text)
        else:
            items.append("")

    return items


def get_bench() -> list[str]:
    bench: list[str] = []

    for i in range(9):
        bench.append(get_bench_slot(i))
    return bench


def get_bench_slot(i: int) -> str:
    unit_name: str = ""

    controller.move((1000, 300))
    controller.move(coordinates.BENCH_COORDS[i])
    time.sleep(0.05)
    text = Image.get_screen_text(coordinates.UNIT_NAME_ON_BENCH_WINDOWS[i], whitelist=Image.ALPHABET_WHITELIST)

    if text in game_info.CHAMPIONS:
        unit_name = text

    controller.move((1000, 300))
    return unit_name


def get_shop() -> list[str]:
    shop: list[str] = []

    for i in range(5):
        text = Image.get_screen_text(coordinates.UNIT_NAME_IN_SHOP_WINDOWS[i], whitelist=Image.ALPHABET_WHITELIST)
        if text in game_info.CHAMPIONS:
            shop.append(text)
        else:
            shop.append("")

    return shop

