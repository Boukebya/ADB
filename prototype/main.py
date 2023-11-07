import time
import json
from  OCR.Detect_imp_sep_block import OCR
from  list_analyse.filtre_liste import filter_list
from list_analyse.match_list_bdd import panier_excel

if __name__ == "__main__":

    #file or files we want to detect text in
    detect_file = [r'image\3.jpg']

    #Allows us to get the duration of the program
    #start_time = time.time()

    OCR(detect_file)
    filter_list()
    panier_excel()
