import PyPDF2
from preproc_data import preprocessing

def get_text_pdf(filename):

    pdffileobj = open(filename,'rb')

    pdfreader=PyPDF2.PdfFileReader(pdffileobj)

    nb_page = pdfreader.numPages

    open('data.txt', 'w').close()

    for i in range(nb_page):

        # Creating a page object
        pageObj = pdfreader.getPage(i)


        # Extracting text from page
        # And splitting it into chunks of lines
        text = pageObj.extractText().split("\n\n")

        # Finally the lines are stored into list
        # For iterating over list a loop is used
        for i in range(len(text)):
            # Printing the line
            # Lines are seprated using "\n"
            with open('data.txt', 'a', encoding="utf-8") as data:
                data.write(text[i])

    preprocessing('data.txt')
    return



if __name__ == "__main__":

    detect_file = r'C:\Users\valen\Desktop\Projet_fourniture\fourniture liste\600878 Kit matériel et options.pdf'

    get_text_pdf(detect_file)