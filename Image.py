import numpy as np
import cv2
from mss import mss
from PIL import ImageGrab, Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


ALPHABET_WHITELIST = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBER_WHITELIST = "0123456789-"
sct = mss()


def grayscale(image: Image) -> Image:
    """Set an image's colors to grayscale"""
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def thresholding(image: Image) -> Image:
    """Set an image's colors to black and white using thresholding"""
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]


def image_array(image: Image) -> []:
    """Converts image to an array"""
    image = np.array(image)
    return image


def resize_image(image: Image, scale: int) -> Image:
    """Scales up/down an image"""
    return image.resize((image.width * scale, image.height * scale))


def get_image_text(image: Image, whitelist: str = "") -> str:
    """Returns the text from the image"""
    resize = resize_image(image, 4)
    array = image_array(resize)
    grayscale_image = grayscale(array)
    thresholding_image = thresholding(grayscale_image)
    text = pytesseract.image_to_string(thresholding_image,
                                       config=f'--psm 7 -c tessedit_char_whitelist={whitelist}').strip()
    return text


def get_screen_text(window: tuple, whitelist: str = "") -> str:
    """Returns the text from the image"""
    image = get_screen(window)
    resize = resize_image(image, 4)
    array = image_array(resize)
    grayscale_image = grayscale(array)
    thresholding_image = thresholding(grayscale_image)
    text = pytesseract.image_to_string(thresholding_image,
                                       config=f'--psm 7 -c tessedit_char_whitelist={whitelist}').strip()
    return text


def get_item_img(item):
    """Given an item name, returns the corresponding image array."""
    return {
        'GiantsBelt': Image.open('images/carousel_items/carousel_belt.png'),
        'RecurveBow': Image.open('images/carousel_items/carousel_bow.png'),
        'NegatronCloak': Image.open('images/carousel_items/carousel_cloak.png'),
        'SparringGlove': Image.open('images/carousel_items/carousel_glove.png'),
        'NeedlesslyLargeRod': Image.open('images/carousel_items/carousel_rod.png'),
        'BFSword': Image.open('images/carousel_items/carousel_sword.png'),
        'TearoftheGoddess': Image.open('images/carousel_items/carousel_tear.png'),
        'ChainVest': Image.open('images/carousel_items/carousel_vest.png')

    }.get(item, Image.open('images/carousel_items/carousel_belt.png'))


def get_image(filepath: str):
    return Image.open(filepath)


def get_drop_img(drop):
    """Given a drop (gray, blue, gold), returns the corresponding image"""
    return {
        'Gray': Image.open('images/misc/gray_drop.png'),
        'Blue': Image.open('images/misc/blue_drop.png'),
        'Gold': Image.open('images/misc/gold_drop.png'),
    }.get(drop, Image.open('images/misc/blue_drop.png'))


def get_screen(window: tuple) -> Image:
    """Returns an image taken from the screen"""
    image = ImageGrab.grab(bbox=window)
    return image


def find_image_on_screen(image: Image, threshold: float, window: tuple) -> (int, int):
    """Returns the x, y coordinate that an image appears on the screen"""
    method = cv2.TM_SQDIFF_NORMED

    screen = get_screen(window)
    screen_array = image_array(screen)
    color = cv2.cvtColor(screen_array, cv2.COLOR_RGB2BGR)
    img_array = image_array(image)
    result = cv2.matchTemplate(img_array, color, method)

    mn, _, mnLoc, _ = cv2.minMaxLoc(result)

    MPx, MPy = mnLoc

    trows, tcols = image.shape[:2]

    if mn <= threshold:
        x, y = MPx + window[0] + int(tcols / 2), MPy + window[1] + int(trows / 2)
        return x, y
    else:
        # NOT FOUND
        return -1, -1


def find_image_on_image(image1: Image, threshold: float, image2: Image) -> (int, int):
    """Returns the x, y coordinate that an image appears on the screen"""
    method = cv2.TM_SQDIFF_NORMED

    screen = image2
    screen_array = image_array(screen)
    color = cv2.cvtColor(screen_array, cv2.COLOR_RGB2BGR)
    img_array = image_array(image1)
    result = cv2.matchTemplate(img_array, color, method)

    mn, _, mnLoc, _ = cv2.minMaxLoc(result)

    MPx, MPy = mnLoc

    trows, tcols = image1.shape[:2]

    if mn <= threshold:
        h, w = image2.shape[:2]
        x, y = MPx + w + int(tcols / 2), MPy + h + int(trows / 2)
        return x, y
    else:
        # NOT FOUND
        return -1, -1




