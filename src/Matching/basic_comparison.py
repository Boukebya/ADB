import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import nltk
from src.Extraction.gpt3_extraction import gpt3_comparaison

def gpt3_matching():

    #open ocr.txt
    with open('ocr.txt', 'r', encoding='utf-8') as file:
        content_ocr = file.read()
    # if content_ocr first line is ```json, remove it
    if content_ocr[0] == "`":
        content_ocr = content_ocr.split("\n")
        content_ocr = content_ocr[1:-1]
        content_ocr = "\n".join(content_ocr)

    # read content_ocr as json
    content_ocr = json.loads(content_ocr)

    #open annuaire
    annuaire = json.load(open("Matching/annuaire2.json", "r", encoding="utf-8"))
    annuaire = annuaire["entities"]

    liste = correspondance_liste(content_ocr, annuaire)
    # put it in ocr.txt
    with open('ocr.txt', 'w', encoding='utf-8') as f:
        json.dump(liste, f, ensure_ascii=False, indent=4)


def correspondance(article, annuaire):
    """
    Compare l'article avec l'annuaire pour trouver une correspondance.
    :param article: article à comparer, dict avec clé 'name'
    :param annuaire: annuaire des articles, liste de dicts avec clés 'texte' et 'type'
    :return: référence de l'article correspondant avec le plus haut score
    """

    # Initialisation des scores pour chaque entité de l'annuaire
    scores = [0] * len(annuaire)

    mots_article = preprocess_string(article["name"])
    sentence =""
    for mot in mots_article:
        sentence += mot + " "
    #print("mots article : ", sentence)

    # Comparaison de chaque mot de l'article avec chaque entité de l'annuaire
    for i, entite in enumerate(annuaire):
        texte_entite = entite["texte"]

        for mot in mots_article:
            if mot in texte_entite:
                scores[i] += 1


    # Trouver l'entité avec le score le plus élevé
    max_score = max(scores)
    if max_score == 0:
        return "none score = 0"
    index_max = scores.index(max_score)
    resultat = annuaire[index_max]

    egalite = []

    # si plusieurs articles ont le même score print
    if scores.count(max_score) > 1:
        iter = 0
        #print("plusieurs articles ont le même score :")
        for i, entite in enumerate(annuaire):
            if scores[i] == max_score:
                egalite.append(entite)
                #print(entite["texte"])
                iter += 1

        resultat = gpt3_comparaison(sentence, egalite)
        resultat = gestion(resultat)
        print(mots_article,"---> ", resultat, "max score : ", max_score, "gpt3", " i;", iter)
    else:
        print(mots_article,"---> ", resultat, "max score : ", max_score)
    return resultat


def correspondance_liste(liste, annuaire) :
    """
    Compare une liste json avec l'annuaire pour trouver une correspondance pour chaque élément de la liste.
    :param liste: liste à comparer, liste de dicts avec clé 'name'
    :param annuaire: annuaire des articles, liste de dicts
    """
    liste_articles = []
    for article in liste:
        liste_articles.append(correspondance(article, annuaire))
    return liste_articles


def gestion(nom_fourniture):
    nom_fourniture = nom_fourniture.lower()
    # retrouver nom_fourniture dans annuaire
    for element in annuaire:
        if element["texte"].lower() == nom_fourniture:
            return element
    return "none_gestion"


def preprocess_string(s):
    """
    Prétraitement d'un article "name" : "element", "nombre" : "element"
    :param s: string à prétraiter
    :return: string prétraitée
    """
    tokens = nltk.word_tokenize(s, language='french')
    tokens = [word for word in tokens if word.lower() not in stopwords.words('french')]
    accent = {"é": "e", "è": "e", "ê": "e", "à": "a", "ç": "c", "ù": "u", "û": "u", "ô": "o", "î": "i", "ï": "i"}
    tokens = [word.lower() for word in tokens]
    tokens = [''.join(accent.get(char, char) for char in word) for word in tokens]
    #print(tokens)
    return tokens


annuaire = json.load(open("Matching/annuaire2.json", "r", encoding="utf-8"))
annuaire = annuaire["entities"]

