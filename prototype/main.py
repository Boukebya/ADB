from OCR.Detect_imp_sep_block import OCR
import time
import tkinter.filedialog as filedialog
import os

if __name__ == "__main__":

    # spawn a pop-up window that allows you to select the file you want to detect text in, pop-up must start in project directory
    root = filedialog.Tk()
    root.withdraw()
    detect_file = filedialog.askopenfilenames(initialdir=os.getcwd(), title="Select file",
                                              filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    root.destroy()

    #Allows us to get the duration of the program
    start_time = time.time()

    # If selected file is an image, we call the OCR function
    if detect_file[0].endswith(".jpg"):
        OCR(detect_file)
    else:
        print("XML, or pdf file not supported yet")

    print("%s seconds to achieve OCR" % (time.time() - start_time))

    # previous
    #filter_list()
    #panier_excel()
