def word_method(list1, list2):
    """
    Method to compare the results of the two OCRs, word by word, delete the words that are the same.
    Score is 1 for same similarity, 0 for no similarity
    """

    counter = 0
    # take each word in google_ocr and find it in tess_ocr
    for word in list1:
        # if the word is the same, add 1 to the counter
        if word in list2:
            counter += 1
            # delete the word from the list to avoid duplicates
            list2.remove(word)
            list1.remove(word)

    return counter / len(list1)


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
    print(google_words)
    print(tess_words)

    score = word_method(google_words, tess_words)
    print(score)
    return score


compare_ocr("recognized.txt", "data.txt")
