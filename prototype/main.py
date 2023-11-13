from OCR.Detect_imp_sep_block import OCR
import time
from prototype.opencv_ocr import opencv_ocr, opencv_ocr_pdf, opencv_ocr_xlsx
from prototype.perf_measurement import compare_ocr


def main_process(detect_file):
    print(detect_file)
    # Allows us to get the duration of the program
    start_time = time.time()

    # If selected file is an image, we call the OCR function
    if detect_file.endswith(".jpg"):
        opencv_ocr(detect_file)
    elif detect_file.endswith(".xlsx"):
        opencv_ocr_xlsx(detect_file)
    elif detect_file.endswith(".pdf") or detect_file.endswith(".doc") or detect_file.endswith(".docx"):
        opencv_ocr_pdf(detect_file)
    else:
        print("File type not supported")

    print("%s seconds to achieve OCR" % (time.time() - start_time))

    return time.time() - start_time


if __name__ == "__main__":
    print("feur")

    # previous
    #OCR(detect_file)
    # filter_list()
    # panier_excel()
