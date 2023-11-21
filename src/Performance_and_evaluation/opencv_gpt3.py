import time
from src.Extraction.gpt3_extraction import gpt3_extraction
from src.OCR.opencv_ocr import opencv_ocr


def test_gptopencv(file_path):
    # use vertex ocr
    start_time = time.time()
    opencv_ocr(file_path)

    gpt3_extraction("ocr.txt")
    print("%s seconds to achieve both things" % (time.time() - start_time))




test_gptopencv("../../images/1.jpg")