import pytesseract
from PIL import Image

# Convert image within box(coordinates) to text
# @param img the screenshot to be converted to text
# @box a 4-tuple defining the left, upper, right, and lower pixel coordinate of region to be ocr'd
# @return 4-character string resulting from the ocr, or an empty string if ocr fails.
def image_to_text(img, box):
    region = img.crop(box)
    # Tesseract works best on small images, so create a thumbnail
    new_dimensions = (120,36)
    region.thumbnail(new_dimensions)
    custom_config = r'--oem 3 --psm 7 '  #  psm  7    Treat the image as a single line
    allowlist = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    custom_config += "-c tessedit_char_whitelist={} ".format(allowlist)
    # do the OCR
    results = pytesseract.image_to_string(region, config=custom_config).strip()

    # if we don't have 4 letters the ocr failed
    if len(results) != 4:
        return "" # Found no text in region
    return results
