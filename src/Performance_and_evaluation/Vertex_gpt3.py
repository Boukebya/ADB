import time

from src.Extraction.gpt3_extraction import gpt3_extraction
from src.OCR.vertex_ocr import vertex_ocr


def test_gptvertex(file_path):
    # use vertex ocr
    start_time = time.time()
    vertex_ocr(file_path)

    gpt3_extraction("ocr.txt")
    print("%s seconds to achieve both things" % (time.time() - start_time))




test_gptvertex("../../images/1.jpg","../Furniture_list/data_1.txt","../Furniture_list/data_extraction1.txt")
