import shutil
import cv2
import pandas as pd
import pytesseract
from ironpdf import *

"""
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
"""

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


def disp_img(img):
    """
    Method to display an image
    :param img: image to display
    """
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def opencv_ocr(img_path):
    """
    Method to extract text from an image file using Tesseract OCR
    :param img_path: path to the image file
    """

    # Read image from which text needs to be extracted
    img = cv2.imread(img_path[0])
    # Convert the image to gray scale to improve contrast for OCR
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Performing OTSU threshold to minimize background noise
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_TOZERO)
    # Use tesseract to extract text from the image
    text = pytesseract.image_to_string(thresh1, lang='fra')
    # print(text)

    # write extracted text to a file
    with open('recognized.txt', 'w', encoding='utf-8') as f:
        f.write(text)


def opencv_ocr_pdf(img_path):
    """
    Method to extract text from a pdf file, It will create a temp folder to store the images of each page of the pdf
    and then extract text from each image using Tesseract OCR.
    :param img_path: path to the pdf file
    """

    # create temp folder to store images
    if not os.path.exists('images/temp'):
        os.makedirs('images/temp')

    # Load the PDF document
    pdf = PdfDocument.FromFile(img_path)
    # Extract all pages to a folder as image files
    pdf.RasterizeToImageFiles("images/temp/*.png", DPI=400)

    # Extract text from each page using Tesseract OCR
    text_data = ''
    for page in os.listdir('images/temp'):
        path = os.path.join("images/temp/", page)

        img = cv2.imread(path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Performing OTSU threshold to minimize background noise
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_TOZERO)
        text = pytesseract.image_to_string(thresh1, lang='fra')
        text_data += text + '\n'

    with open('recognized.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    # delete the temp folder
    shutil.rmtree('images/temp')


def opencv_ocr_xlsx(img_path):
    """
    Method to extract text from a xlsx file, and keeping the same format as the original file
    :param img_path: path to the xlsx file
    """

    with open('recognized.txt', 'w', encoding='utf-8') as file:
        pd.read_excel(img_path).to_string(file, index=False)
