import time

from src.Extraction.gpt3_extraction import gpt3_extraction
from src.OCR.gpt4 import use_gpt4
from src.OCR.opencv_ocr import opencv_ocr
from src.OCR.vertex_ocr import vertex_ocr
from src.Performance_and_evaluation.perf_measurement import compare_ocr


def test_gptvertex(file_path,file_verif,file_extract):
    # use vertex ocr
    start_time = time.time()
    vertex_ocr(file_path)
    score = compare_ocr("ocr.txt",file_verif)
    gpt3_extraction("ocr.txt")
    score_extract = compare_ocr(file_extract,"ocr.txt")
    print("%s seconds to achieve both things" % (time.time() - start_time))
    print("Score vertex :", score)
    print("Score gpt3 :", score_extract)

    return score, score_extract


def test_gptopencv(file_path,file_verif,file_extract):
    # use vertex ocr
    start_time = time.time()
    opencv_ocr(file_path)
    score = compare_ocr("ocr.txt",file_verif)
    gpt3_extraction("ocr.txt")
    score_extract = compare_ocr(file_extract,"ocr.txt")
    print("%s seconds to achieve both things" % (time.time() - start_time))
    print("Score vertex :", score)
    print("Score gpt :", score_extract)

    return score, score_extract

def test_gpt4(file_path,file_verif,file_extract):
    # use vertex ocr
    start_time = time.time()
    use_gpt4(file_path)
    score = compare_ocr("ocr.txt",file_extract)
    print("%s seconds to achieve both things" % (time.time() - start_time))
    print("Score gpt4 :", score)

    return score

data1 = test_gptvertex("../../images/1.jpg","../Furniture_list/data_1.txt","../Furniture_list/data_extraction_1.txt")

