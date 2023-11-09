from OCR.Detect_imp_sep_block import OCR
import time
import tkinter.filedialog as filedialog
import os
from prototype.opencv_ocr import opencv_ocr, opencv_ocr_pdf, opencv_ocr_xlsx
from prototype.perf_measurement import compare_ocr


def file_dial():
    """
    Method to open a file dialog and select a file, return the path of the file
    """
    root = filedialog.Tk()
    root.withdraw()
    # open file dialog with pdf, jpg, xml, doc, docx
    detect_file = filedialog.askopenfilenames(initialdir=os.getcwd(), title="Select file",
                                                filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    root.destroy()
    return detect_file


if __name__ == "__main__":

    compare_ocr("data.txt","data.txt")
    detect_file = file_dial()

    #Allows us to get the duration of the program
    start_time = time.time()

    # If selected file is an image, we call the OCR function
    if detect_file[0].endswith(".jpg"):
        opencv_ocr(detect_file)
    elif detect_file[0].endswith(".xlsx"):
        opencv_ocr_xlsx(detect_file[0])
    elif detect_file[0].endswith(".pdf") or detect_file[0].endswith(".doc") or detect_file[0].endswith(".docx"):
        opencv_ocr_pdf(detect_file[0])
    else:
        print("File type not supported")

    print("%s seconds to achieve OCR" % (time.time() - start_time))

    # previous
    # OCR(detect_file)
    # filter_list()
    # panier_excel()
