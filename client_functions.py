import Image
import coordinates
import controller


def accept_queue() -> None:
    accept_img = Image.get_image("images/misc/accept_queue.png")

    while not game_start():
        location = Image.find_image_on_screen(accept_img, 0.2, coordinates.SCREEN_WINDOW)
        if location != (-1, -1):
            controller.click(location)


def game_start() -> bool:
    img = Image.get_image("images/misc/start_stage.png")
    location = Image.find_image_on_screen(img, 0.1, coordinates.SCREEN_WINDOW)
    return location != (-1, -1)