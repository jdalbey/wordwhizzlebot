from unittest import TestCase
from Board import get_cell_location
from Board import get_letter_box
from Board import get_ocr_text
from Board import find_candidate_words
from PIL import Image

# Unit tests for Board class
class Test(TestCase):

    def test_get_cell_location(self):
        assert (251, 624) == get_cell_location(1, 1)
        assert (443, 624) == get_cell_location(1, 2)
        assert (635, 624) == get_cell_location(1, 3)
        assert (827, 624) == get_cell_location(1, 4)
        assert (251, 816) == get_cell_location(2, 1)
        assert (443, 816) == get_cell_location(2, 2)

    def test_get_letter_box(self):
        assert (215, 546.0, 286, 654.0) == get_letter_box(1, 1)
        assert (791, 1122.0, 862, 1230.0) == get_letter_box(4, 4)

    def test_get_ocr_text(self):
        img = Image.open("4x4board.jpg").convert('L')
        assert ['HOTG','NUSG','ADKX','JULY'] == get_ocr_text(img)

    def test_find_candidate_words(self):
        data = [['B','I','G','X'],['I','A','G','X'],['R','I','T','X'],['D','I','G','X']]
        assert ('BIG', (1, 1, 1, 3)) == find_candidate_words(data)[0]
        assert ('BIGX', (1, 1, 1, 4)) == find_candidate_words(data)[1]
        assert ('BIR', (1, 1, 3, 1)) == find_candidate_words(data)[2]
        print (find_candidate_words(data))

