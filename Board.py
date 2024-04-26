from PIL import Image
import Image_ocr

# This module represents the puzzle board on the phone screen.
# It defines constants, conversion functions, and converting from image to text

# Constants for the phone screen, given a resolution of 1080x2400.
size = 4    # number of rows and columns
topleft = (165,510)  # coordinate of topleft corner of board
cellwidth = 172      # width of a cell on the board
cellheight = 180     # height of a cell on the board
hgap = 20            # horizontal gap between cells
vgap = 12            # vertical gap between cells
rowoffset = cellheight + vgap   # distance between rows
coloffset = cellwidth + hgap    # distance between columns
topmargin = cellheight / 5      # distance from top of cell to letter
bottommargin = cellheight / 5   # distance from bottom of cell to letter
leftmargin = 50                 # distance from left edge of cell to letter
rightmargin = 121               # distance from right edge of cell to letter

# Utility methods that compute region boundaries in a puzzle board
# NB: row and columns are 1-based !!!

# Get the coordinates of a box around a single letter on the board
# This box is tighter to the letter than the cell boundaries
# @pre 1 <= rownum <= 4
# @pre 1 <= gapnum <= 4
# @return x1,y1,x2,y2 defining the upper left and lower right corners of the box
def get_letter_box(row,col):
    y1 = topleft[1] + rowoffset * (row - 1) + topmargin
    x1 = topleft[0] + coloffset * (col - 1) + leftmargin
    y2 = topleft[1] + rowoffset * (row - 1) + topmargin * 4
    x2 = topleft[0] + coloffset * (col - 1) + rightmargin
    return (x1,y1,x2,y2)

# Get the coordinates of the center of a cell, given its row,col address in the array
# This is used to locate where a swipe can start or end.
# NB: row,col are 1-based !!!
# @pre 1 <= rownum <= 4
# @pre 1 <= gapnum <= 4
# @return x1,y1 defining the location of the center of the cell
def get_cell_location(row,col):
    y = topleft[1] + rowoffset * (row - 1) + topmargin + cellheight / 2 - vgap
    x = topleft[0] + (coloffset * col) - hgap - cellwidth / 2
    return int(x),int(y)

# Perform OCR on an image of the board and convert it to text.
# @param img is a screencapture of the game screen
# @return a list of four strings, each of which holds the text that was OCR'd from one row of the image.
def get_ocr_text(img):
    rows_text = []
    # Isolate one row of the board
    for row in range(1,5):
        # Create a blank white image on which the letters can be placed
        mergedImg = Image.new("L", (350, 108), "white")
        # Extract each letter in the row
        for col in range(1, 5):
            # Determine the coordinates of the box that bounds the letter
            letterbox = get_letter_box(row, col)
            # Crop the image to the size of the letter
            letter = img.crop(letterbox)
            # paste the letter into a slightly larger blank image
            mergedImg.paste(letter, (5 + (71 * (col - 1)), 0))

        # The merged image has all 4 letters placed adjacent
        # Perform OCR on the image of four letters
        result = Image_ocr.image_to_text(mergedImg, (0,0,350,108))
        print (result)
        # Append the ocr text to a list
        rows_text.append(result)
    return rows_text

# Extract all the possible strings from the board.
# Consider each letter and traveling in all eight adjacent directions.
# @param 4 x 4 array of the letters on the board
# @return a list of tuples. The first element is a string, the second is a tuple defining the start and end positions
# of the string in the array.    E.g., ("HOT", (1, 1, 1, 3))  indicates that the string "HOT" starts in position (1,1)
# and ends in position (1,3) in the array.
def find_candidate_words(array):
    result = []

    # Get the dimensions of the array
    rows, cols = len(array), len(array[0])

    # Iterate through each element in the array
    for row in range(rows):
        for col in range(cols):
            # Get the starting letter for the string we're building
            original_element = array[row][col]

            # Iterate through the eight adjacent cells
            for x_offset in range(-1, 2):
                for y_offset in range(-1, 2):
                    # Skip the center cell
                    if x_offset == 0 and y_offset == 0:
                        continue

                    adjacent_string = original_element  # Start with the original element

                    # Iterate in the same direction until the edge of the array is reached
                    x, y = row + x_offset, col + y_offset
                    startx, starty = row, col
                    while 0 <= x < rows and 0 <= y < cols:
                        adjacent_string += array[x][y] # Append a letter to the string
                        # Add to the result list if the string length is 3 or more (only 3-letter words are legal)
                        if len(adjacent_string) >= 3:
                            result.append((adjacent_string,(startx+1,starty+1,x+1,y+1)))
                        x += x_offset
                        y += y_offset

    return result