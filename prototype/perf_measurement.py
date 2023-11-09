def word_method(list1, list2):
    """
    Method to compare the results of the two OCRs, word by word, delete the words that are the same.
    Score is 1 for same similarity, 0 for no similarity
    """

    counter = 0
    # order list
    list1.sort()
    list2.sort()

    #print(list1)
    #print(list2)

    #print("List1 :",len(list1), "List2 :", len(list2))

    no_match = []
    # take each word in google_ocr and find it in tess_ocr
    for word in list1:
        # if the word is the same, add 1 to the counter
        if word in list2:
            counter += 1
            # remove the word from the list
            list2.remove(word)

        else:
            no_match.append(word)
            list1.remove(word)

    #print("Words that are still in lists (no matching) :",len(no_match))
    #print(no_match)
    #print("lists:")
    #print(list1)
    #print(list2)

    return counter / (len(list1))


def split_text(text):
    """
    Split texts into words
    :param text: path to the text file
    :return: list of words
    """
    texte = []
    with open(text, 'r', encoding='utf-8') as f:
        for line in f:
            texte.append(line.strip())
    words_list = []
    for sentence in texte:
        # split the sentence into words
        words = sentence.split()
        # append each word to the list of words
        for word in words:
            # If words anything else than characters, numbers or punctuation, skip it
            if word.isalnum() and word.isascii():
                words_list.append(word)

    return words_list


def compare_ocr(google_ocr, tess_ocr):
    """
    Method to compare the results of the two OCRs
    :param google_ocr: Path to text extracted by Google OCR
    :param tess_ocr: Path to text extracted by Tesseract OCR
    """

    google_words = split_text(google_ocr)
    tess_words = split_text(tess_ocr)

    score = word_method(google_words, tess_words)
    print(score, ", This score represents how much of the words in list 1 are present in list 2."
                 "\nNote that the score is measured by finding the same words in the two lists, not the same order"
                 "\nbased on the first list. If the first list is longer than the second, the score will be lower"
                 "\nbecause the first list is the reference.")
    return score


compare_ocr("recognized.txt", "data.txt")
