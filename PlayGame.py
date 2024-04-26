#!/usr/bin/python3
import time
from ppadb.client import Client as AdbClient
from PIL import Image
import Board
import Words

# This project is a small demonstration of a bot that plays an Android mobile game, Word Whizzle.
# This file contains the main routine and several helper functions.

# Connect to an Android device attached by USB cable
# @return a descriptor to the connected device, or 0 if no device found.
def connect():
    devices = []
    client = AdbClient(host="127.0.0.1", port=5037)
    try:
        devices = client.devices()
    except Exception as e:
        print(e)
        print ("You might need to run 'adb start-server' command in a terminal window.")
        exit()
    # Are any devices connected?
    if len(devices) == 0:
        print('No devices found.')
        return 0

    device = devices[0]  # return the first device found
    print(f'Found device: {device}')
    if device.wm_size().width != 1080 or device.wm_size().height != 2400:
        print ("Sorry, this demo only works on screens of size 1080x2400")
        exit()
    return device

# Capture the current screen displayed on the Android device
# @return Image of the screen
def screen_capture():
    result = device.screencap()
    # write the binary data to a PNG file
    with open("images/screen.png", "wb") as fp:
        fp.write(result)
    # read the image file and return it
    return Image.open("images/screen.png")

# Convert a list of four strings, each 4-characters long, into a 2d array
# This converts the text resulting from OCR into a representation of a 4x4 board.
def convert_to_array(string_list):
    # Assuming each string in the list is 4 characters long
    rows = cols = 4
    # initialize a 2d array
    array_2d = [[0 for i in range(cols)] for j in range(rows)]
    # Convert a list of 4-letter strings to a 2D array
    for i in range(rows):
        for j in range(cols):
            array_2d[i][j] = string_list[i][j]
    return array_2d

# Play a single puzzle in the game.
# It will attempt to read the letters of the puzzle and then swipe any dictionary words it finds.
def solve_puzzle(img):
    # OCR the screen image to extract the letters comprising the puzzle.
    puzzle_letters = Board.get_ocr_text(img)

    # Convert the strings into a 4x4 grid
    grid = convert_to_array(puzzle_letters)

    # Create a list of potential solution words from the grid of letters
    candidate_list = Board.find_candidate_words(grid)
    #print(candidate_list)

    # Evaluate the candidates to get the actual, dictionary words.
    legal_words = Words.get_legal_words(candidate_list)

    # Perform a swipe for each legal word
    for candidate in legal_words:
        word, route = candidate
        print(word, route)
        # Get the coordinates for the swipe start and end
        swipestart = Board.get_cell_location(route[0], route[1])
        swipeend =  Board.get_cell_location(route[2], route[3])
        # Do the swipe on the puzzle
        device.shell(f'input swipe {swipestart[0]} {swipestart[1]} {swipeend[0]} {swipeend[1]}  250 ')
        time.sleep(0.5) # delay to allow animation to complete

# Entry point for the application
# Assumes the Word Whizzle game is showing a 4x4 puzzle that hasn't been solved.
if __name__ == '__main__':
    #Go connect to device
    device = connect()
    # If a device is connected, grab its screen display
    if device != 0:
        img = screen_capture()
    else:
        # If we aren't connected, use this image for testing
        img = Image.open("tests/4x4board.jpg").convert('L')

    #Go solve the puzzle
    solve_puzzle(img)
