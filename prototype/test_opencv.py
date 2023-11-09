import cv2
import pytesseract
from PIL import Image
import os


def test():
    # Convert the image to gray scale to improve contrast for OCR
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold to minimize background noise
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    # Specify structure shape and kernel size for morphological operations
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (14, 14))

    # Applying dilation on the threshold image to emphasize text
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=8)
    # Si on met iteration = 1, on obtient une bb pour chaque mot, 8 c'est pas mal pour les résultats sinon

    # Finding contours to detect individual text blocks
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Creating a copy of the image to draw rectangles around text
    im2 = img.copy()

    # Looping through the identified contours and extracting text
    extracted_texts = []  # A list to hold extracted texts for display

    i = 0
    for cnt in contours:
        # Get the bounding box coordinates from the contour
        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image around the text
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for OCR
        cropped = im2[y:y + h, x:x + w]
        # create a folder to store the cropped images
        # create folder
        if not os.path.exists('images/cropped'):
            os.makedirs('images/cropped')
        # save cropped images, with custom names
        cv2.imwrite('images/cropped/' + str(i) + '.jpg', cropped)

        # Apply OCR on the cropped image, for french language
        text = pytesseract.image_to_string(cropped, lang='fra')

        # if text empty or contains only spaces, skip it
        if text.isspace() or text == '':
            # delete the cropped image
            os.remove('images/cropped/' + str(i) + '.jpg')
            continue

        # Append the text into the list
        extracted_texts.append(text)
        i += 1

    # Save the image with rectangles to visualize the areas processed by OCR
    cv2.imwrite('images/processed_image.jpg', im2)

    # Return the list of extracted texts
    extracted_texts = [text for text in extracted_texts if text != '']
    print(extracted_texts)

    # write extracted text to a file
    with open('recognized.txt', 'w', encoding='utf-8') as f:
        # loop from the end of the list to the beginning
        for text in extracted_texts[::-1]:
            f.write(text + '\n')


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

# Read image from which text needs to be extracted
img = cv2.imread("images/1.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Performing OTSU threshold to minimize background noise
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_TOZERO)

# resize img
# imgdisp = cv2.resize(thresh1, (800,800))
cv2.imshow('imgdisp', gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow('imgdisp', thresh1)
cv2.waitKey(0)
cv2.destroyAllWindows()

text = pytesseract.image_to_string(thresh1, lang='fra')

print(text)

# write extracted text to a file
with open('recognized.txt', 'w', encoding='utf-8') as f:
    f.write(text)
