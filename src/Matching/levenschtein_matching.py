import re
import fuzzywuzzy
import nltk
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
from nltk.corpus import stopwords

def get_best_match(str, annuaire):

    # if annuaire is only one article
    if type(annuaire) == dict :
        return annuaire
    # if annuaire is nonetype
    if annuaire == None:
        print(str["name"]," --> ", "article non trouvé dans best match ")
        return {"texte": "article non trouvé dans best match ", "rÃ©fÃ©rence": "none"}

    scores = []
    for article in annuaire:
        scores.append(fuzz.ratio(str["name"], article["texte"]))
    max_score = max(scores)
    #print(max_score)


    # return a random article with max score
    for i, article in enumerate(annuaire):
        if scores[i] == max_score and max_score > 20:
            print(str["name"]," --> ", article["texte"], " : ", max_score)
            return article

    return {"texte": "article non trouvé levenschtein", "rÃ©fÃ©rence": "none"}


def preprocess_string(s):
    """
    Prétraitement d'un article "name" : "element", "nombre" : "element"
     enlève les accents, les caractères spéciaux, tokenize, stopwords, minuscule
    :param s: string à prétraiter
    :return: string prétraitée
    """

    # remplacer les accents
    accent = {"é": "e", "è": "e", "ê": "e", "à": "a", "ç": "c", "ù": "u", "û": "u", "ô": "o", "î": "i", "ï": "i"}
    for key, value in accent.items():
        s = s.replace(key, value)
    # print(s)

    # remplacer les caractères spéciaux par des espaces
    tokens = re.sub(r"[^a-zA-Z0-9]", " ", s)
    # print(tokens)

    # tokenize
    tokens = nltk.word_tokenize(tokens, language='french')

    # supprimer les stopwords
    tokens = [word for word in tokens if word.lower() not in stopwords.words('french')]
    # print(tokens)

    # mettre en minuscule
    tokens = [word.lower() for word in tokens]
    # print(tokens)
    # lemmatization
    #tokens = [nlp(word)[0].lemma_ for word in tokens]
    # print(tokens)
    return tokens


def correspondance_pre(article, annuaire):
    """
    Compare l'article avec l'annuaire pour trouver une correspondance.
    :param article: article à comparer, dict avec clé 'name'
    :param annuaire: annuaire des articles, liste de dicts avec clés 'texte' et 'type'
    :return: référence de l'article correspondant avec le plus haut score
    """

    # Initialisation des scores pour chaque entité de l'annuaire
    scores = [0] * len(annuaire)

    mots_article = preprocess_string(article["name"])
    important_word = preprocess_string(article["article"])
    sentence = ""
    imp_word = ""


    for mot in mots_article:
        sentence += mot + " "
    for mot in important_word:
        imp_word += mot + " "

    #print(sentence)
    #print(imp_word)

    # Comparaison de chaque article dans l'annuaire avec chaque mot de l'article que l'on cherche à comparer
    for i, article in enumerate(annuaire):
        texte_entite = article["texte"]

        if imp_word in texte_entite:
            scores[i] += 3
        else:
            scores[i] -= 2

        # score = nombre de mots de l'article qui sont dans l'entité
        for mot in mots_article:
            # score + 1 si le mot est dans l'article de l'annuaire

            if mot in texte_entite:
                scores[i] += 1

    # Trouver l'entité avec le score le plus élevé
    max_score = max(scores)
    #print(max_score)

    # Si aucun score n'est supérieur à 0, il n'y a pas de correspondance
    if max_score <= 0:
        print(sentence, " --> ", "Aucun score > 0 ")
        out = {"texte": "Aucun score > 0 ", "rÃ©fÃ©rence": "none"}
        return out

    # Trouver l'index de l'entité avec le score le plus élevé
    index_max = scores.index(max_score)
    resultat = annuaire[index_max]


    articles_score_max = []
    # si plusieurs articles ont le même score on utilise gpt3 pour les départager
    if scores.count(max_score) >= 1:
        iter = 0

        # si plusieurs articles ont le même score, on les met dans la liste
        for i, article in enumerate(annuaire):
            if scores[i] == max_score:
                articles_score_max.append(article)
                # print(entite["texte"])
                iter += 1

        return articles_score_max


def correspondance(content_extraction, annuaire):
    """
    Compare une liste json d'extraction avec l'annuaire pour trouver une correspondance pour chaque élément de la liste.
    :param liste: liste à comparer, liste de dicts avec clé 'name'
    :param annuaire: annuaire des articles, liste de dicts
    :return: liste des références des articles correspondants
    """
    listes_pre = []
    liste_articles = []

    for article in content_extraction:
        liste_articles.append(correspondance_pre(article, annuaire))

    i= 0
    for article in content_extraction:
        listes_pre.append(get_best_match(article, liste_articles[i]))
        i += 1

    return listes_pre


def use_levenschtein():
    with open('ocr.txt', 'r', encoding='utf-8') as file:
        content_ocr = file.read()
    # if content_ocr first line is ```json, remove it
    if content_ocr[0] == "`":
        content_ocr = content_ocr.split("\n")
        content_ocr = content_ocr[1:-1]
        content_ocr = "\n".join(content_ocr)

    # read content_ocr as json
    content_extraction = json.loads(content_ocr)


    with open('src/Matching/annuaire3.json') as json_file:
        annuaire = json.load(json_file)

    listes_articles = correspondance(content_extraction, annuaire)


    # write file "result.txt" with all articles
    with open('result.txt', 'w', encoding='utf-8') as file:
        for article in listes_articles:
            if article != {"texte": "article non trouvé"}:
                    file.write(article["texte"])
                    file.write(article["rÃ©fÃ©rence"])
                    file.write("\n")


#use_levenschtein()