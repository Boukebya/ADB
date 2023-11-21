import shutil
import cv2
import pandas as pd
import pytesseract
from ironpdf import *

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
    img = cv2.imread(img_path)
    if img is None:
        print("Image not found")
        return

    # Convert the image to gray scale to improve contrast for OCR
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold to minimize background noise
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_TOZERO)

    # Use tesseract to extract text from the image
    text = pytesseract.image_to_string(thresh1, lang='fra')
    # print(text)

    # write extracted text to a file
    with open('../recognized.txt', 'w', encoding='utf-8') as f:
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

    with open('../recognized.txt', 'w', encoding='utf-8') as f:
        f.write(text)

    # delete the temp folder
    shutil.rmtree('images/temp')


def opencv_ocr_xlsx(img_path):
    """
    Method to extract text from a xlsx file, and keeping the same format as the original file
    :param img_path: path to the xlsx file
    """

    with open('../recognized.txt', 'w', encoding='utf-8') as file:
        pd.read_excel(img_path).to_string(file, index=False)
