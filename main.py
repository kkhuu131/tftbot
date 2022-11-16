import Image
import coordinates
import comp


def main():
    print(Image.get_screen_text(coordinates.GOLD_WINDOW, whitelist=Image.NUMBER_WHITELIST))

    for i in range(5):
        print(Image.get_screen_text(coordinates.UNIT_NAME_IN_SHOP_WINDOWS[i], whitelist=Image.ALPHABET_WHITELIST))


if __name__ == "__main__":
    main()
