from OCR.Detect_imp_sep_block import OCR
import time
import tkinter.filedialog as filedialog
import os
from prototype.opencv_ocr import opencv_ocr, opencv_ocr_pdf, opencv_ocr_xml

if __name__ == "__main__":

    # spawn a pop-up window that allows you to select the file you want to detect text in, pop-up must start in project directory
    root = filedialog.Tk()
    root.withdraw()
    # open file dialog with pdf, jpg, xml, doc, docx
    detect_file = filedialog.askopenfilenames(initialdir=os.getcwd(), title="Select file",
                                                filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    root.destroy()

    #Allows us to get the duration of the program
    start_time = time.time()

    # If selected file is an image, we call the OCR function
    if detect_file[0].endswith(".jpg"):
        opencv_ocr(detect_file)
    elif detect_file[0].endswith(".xlsx"):
        opencv_ocr_xml(detect_file[0])
    elif detect_file[0].endswith(".pdf") or detect_file[0].endswith(".doc") or detect_file[0].endswith(".docx"):
        opencv_ocr_pdf(detect_file[0])
    else:
        print("File type not supported")

    print("%s seconds to achieve OCR" % (time.time() - start_time))


    # previous
    #OCR(detect_file)
    #filter_list()
    #panier_excel()
