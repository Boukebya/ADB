from pathlib import Path
import sys
sys.path.append(str(Path.cwd())+'\project_env\Lib\site-packages')
import os
from enum import Enum
import io
import time
from PIL import Image
from google.cloud import vision
from OCR.preproc_data import preprocessing

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\rowan\Downloads\autour-du-bureau-detection.json"

#Utility is to know the type of a block -> what is inside
class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5

#Allows you to get the bounding boxes of every element in the document, may it be from symbols to blocks
def get_document_bounds(document, feature):

    bounds = []

    #Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:

                        if feature == FeatureType.SYMBOL:
                            bounds.append(symbol.bounding_box)

                    if feature == FeatureType.WORD:
                        bounds.append(word.bounding_box)

                if feature == FeatureType.PARA:
                    bounds.append(paragraph.bounding_box)

            if feature == FeatureType.BLOCK:
                bounds.append(block.bounding_box)

    # The list `bounds` contains the coordinates of the bounding boxes.
    return bounds


#Makes it possible to get the text within a bounding box
def text_within(document,x1,y1,x2,y2):

  text = ""

  for page in document.pages:
    for block in page.blocks:
      for paragraph in block.paragraphs:
        for word in paragraph.words:
          for symbol in word.symbols:

            min_x=min(symbol.bounding_box.vertices[0].x,symbol.bounding_box.vertices[1].x,symbol.bounding_box.vertices[2].x,symbol.bounding_box.vertices[3].x)
            max_x=max(symbol.bounding_box.vertices[0].x,symbol.bounding_box.vertices[1].x,symbol.bounding_box.vertices[2].x,symbol.bounding_box.vertices[3].x)
            min_y=min(symbol.bounding_box.vertices[0].y,symbol.bounding_box.vertices[1].y,symbol.bounding_box.vertices[2].y,symbol.bounding_box.vertices[3].y)
            max_y=max(symbol.bounding_box.vertices[0].y,symbol.bounding_box.vertices[1].y,symbol.bounding_box.vertices[2].y,symbol.bounding_box.vertices[3].y)

            if(min_x >= x1 and max_x <= x2 and min_y >= y1 and max_y <= y2):

                text+=symbol.text

                if(symbol.property.detected_break.type==1 or symbol.property.detected_break.type==3):
                    text+=' '
                if(symbol.property.detected_break.type==2):
                    text+='\t'
                if(symbol.property.detected_break.type==5):
                    text+='\n'
    #Sometimes it doesn't insert a '\n' at the end of a block if it doesn't perceive it, so we add it manually, those
    # who shouldn't be there will be deleted by the processing function
    text+="\n"


    return text


#Kind of main function which calls the client (Google Cloud here), create or replace data.txt file and write in it
def render_doc_text(filein):

    """Returns document bounds given an image."""
    client = vision.ImageAnnotatorClient()

    with io.open(filein, "rb") as image_file:
        content = image_file.read()

    #create and/or reset the data file
    open('data.txt', 'w').close()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    #getting the bounding boxes of the bloc of texts in the file (per paragraphs here)
    bounds = get_document_bounds(document, FeatureType.PARA)

    #numbers is here to keep the numbers when they are alone
    numbers = []

    #We have to take only the extremums of the coordinates of the bounding box to get the whole text in it
    for bound in bounds:

        min_x=min(bound.vertices[0].x,bound.vertices[1].x,bound.vertices[2].x,bound.vertices[3].x)
        max_x=max(bound.vertices[0].x,bound.vertices[1].x,bound.vertices[2].x,bound.vertices[3].x)
        min_y=min(bound.vertices[0].y,bound.vertices[1].y,bound.vertices[2].y,bound.vertices[3].y)
        max_y=max(bound.vertices[0].y,bound.vertices[1].y,bound.vertices[2].y,bound.vertices[3].y)
        text = text_within(document, min_x, min_y,max_x, max_y)


        #if there is only one caracter, it is often a number alone not linked to its sentence, so we keep it a concatenate it later
        if len(text) == 2:
            numbers.append(text)

        else :
            if numbers != []:

                num = numbers[0]
                numbers.pop(0)

                with open('data.txt', 'a', encoding="utf-8") as f:
                    f.write(num.rstrip('\n') + " " + text)
            #if it is a sentence we just write it in the data file
            else :

                with open('data.txt', 'a', encoding="utf-8") as f:
                    f.write(text)

    #Allows us to parse the data file while encountering some characters (expecially ",", " et ", " ou ", "+")
    preprocessing('data.txt')

#Allows you to concatenate two images vertically
def get_concat_v(image1, image2):
    im1 = Image.open(image1)
    im2 = Image.open(image2)
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

#Allows you to concatenate two images horizontally
def get_concat_h(image1, image2):
    im1 = Image.open(image1)
    im2 = Image.open(image2)
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def OCR(file):
    #if there is more than one file in entry we need to merge them into one
    if len(file) > 1:

        img_fin = get_concat_h(file[0],file[1])
        img_fin.save("recto-verso\\final.jpg")

        for i in range(2,len(file)):
            img_fin = get_concat_h("recto-verso\\final.jpg",file[i])

        img_fin.save("recto-verso\\final.jpg")

        render_doc_text("recto-verso\\final.jpg")

    #if not we just launch the function
    else:
        render_doc_text(file[0])


# if __name__ == "__main__":

    # #file or files we want to detect text in
    # detect_file = [r'C:\Users\valen\Desktop\1-bis.jpg']
    #
    # #Allows us to get the duration of the program
    # start_time = time.time()
    #
    # OCR(detect_file)
    #
    # #Allows us to know the how much time the program ran
    # print("--- %s seconds ---" % (time.time() - start_time))
