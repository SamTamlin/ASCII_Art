from PIL import Image
from numpy import asarray
from time import sleep
import os


def image_menu():
    """Asks the user to choose an image, loads the selected image and returns
    it as an array."""
    while True:
        print("\t IMAGE SELECTION")
        print("\t[1] Beach ball")
        print("\t[2] Pineapple")
        print("\t[3] Cat")
        print("\t[4] Zebra")
        print("\t[5] Flower")
        print("\n\t[q] Quit")
        user_input = input(
            "\tEnter the number of the photo you wish to view: ").lower()

        if user_input == '1':
            return load_file('beachball.jpg')

        elif user_input == '2':
            return load_file('ascii-pineapple.jpg')

        elif user_input == '3':
            return load_file('cat.jpg')

        elif user_input == '4':
            return load_file('zebra.jpg')

        elif user_input == '5':
            return load_file('flower.jpg')

        elif user_input == 'q':
            print("Good bye")
            return False

        else:
            print("Sorry I didn't understand that.")
            sleep(3)


def load_file(file_name):
    try:
        loaded_image = Image.open(file_name)
        loaded_image = loaded_image.resize((400, 140))
        print("Successfully loaded image!")
        print("Image size: %d x %d"
              % (loaded_image.width, loaded_image.height))
        return loaded_image

    except FileNotFoundError:
        print("sorry I could not load the image.")
        return False


def filter_menu():
    """Asks the user to choose a filter and returns an array with the correct
    'intensity'."""
    while True:
        print("\n\tFILTER SELECTION")
        print("\t[1] Average Brightness")
        print("\t[2] Average Lightness")
        print("\t[3] Average Luminosity")
        filter_choice = input("\tPlease choose a filter: ")

        if filter_choice == '1':
            # Get average brightness from array.
            return get_ave_brightness(pixel_array)

        elif filter_choice == '2':
            # Get average lightness from array.
            return get_ave_lightness(pixel_array)

        elif filter_choice == '3':
            # Get average luminosity from array.
            return get_luminosity(pixel_array)

        else:
            print("Sorry I didn't understand that.")
            sleep(3)


def invert_question(array):
    """Asks user if they would like the picture to be inverted and returns
    the received array inverted if user enters 'y'."""
    while True:
        invert = input(
            "\n\tWould you like the picture inverted? y/n? ").lower()
        if invert == 'y':
            return invert_intensity(array)
        elif invert == 'n':
            return array
        else:
            print("\tSorry I didn't understand that.")
            sleep(3)


def invert_intensity(array):
    inverted = []
    inverted_cells = []
    for lines in array:
        for cells in lines:
            # Invert RGB values by taking them away from 255.
            inverted_cells.append(255 - cells)
    inverted.append(inverted_cells)

    return inverted


def get_ave_brightness(array):
    level = []
    for lines in array:
        for cells in lines:
            # Add mean average of RGB channels to level.
            level.append((int(cells[0]) + int(cells[1]) +
                          int(cells[2])) / 3)
    return level


def get_ave_lightness(array):
    level = []
    for lines in array:
        for cells in lines:
            # Find average of largest & smallest RGB values, & add to level.
            level.append((max(cells) + min(cells)) / 2)
    return level


def get_luminosity(array):
    level = []
    for lines in array:
        for cells in lines:
            # Get weighted ave of RGB values, accounting for human perception:
            # Values are 0.21 R + 0.72 G + 0.07 B
            level.append(
                cells[0] * 0.21 + cells[1] * 0.72 + cells[2] * 0.07)
    return level


ascii_chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW" \
              "&8%B@$"

running = True

while running:
    # Ask user to select an image.
    user_image = image_menu()

    # If False has been returned the program stops.
    if not user_image:
        running = False

    # If running is still True the program continues.
    if running:
        # Convert user_image into an array.
        pixel_array = asarray(user_image)

        pixel_array = invert_question(pixel_array)

        intensity = filter_menu()

        os.system('cls')

        # Scale the brightness with the length of ascii_chars.
        scale = []
        for amount in intensity:
            if amount != 0:
                scale.append((len(ascii_chars)) / (255 / amount))
            else:
                scale.append(1)

        # Round each number in scale to the nearest whole number.
        rounded_scale = [round(item) for item in scale]

        # Match ascii characters to the brightness of the picture.
        ascii_string = ''
        for pixel in rounded_scale:
            ascii_string += (ascii_chars[pixel - 1])

        # Using ascii-string, create a nested list matching the user_image.
        ascii_picture = []
        for cell_number, x in enumerate(ascii_string):
            # If the cell_number is divisible by the width of user_image.
            if (cell_number % user_image.width) == 0:
                # Add a list of that line to the picture.
                ascii_picture.append(ascii_string[(
                                cell_number - user_image.width): cell_number])

        # Print each line of the ascii_picture.
        for line in ascii_picture:
            print(line)
