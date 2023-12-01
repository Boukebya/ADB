import json
import spacy
from nltk.corpus import stopwords
import re
import nltk
from Extraction.gpt3_extraction import gpt3_comparaison


def gpt3_matching():
    """
    Compare les articles de ocr.txt avec l'annuaire pour trouver une correspondance.
    Copie dans ocr.txt les correspondances trouvées.
    """
    # open ocr.txt
    with open('ocr.txt', 'r', encoding='utf-8') as file:
        content_ocr = file.read()
    # if content_ocr first line is ```json, remove it
    if content_ocr[0] == "`":
        content_ocr = content_ocr.split("\n")
        content_ocr = content_ocr[1:-1]
        content_ocr = "\n".join(content_ocr)

    # read content_ocr as json
    content_ocr = json.loads(content_ocr)

    # open annuaire
    annuaire = json.load(open("src/Matching/annuaire2.json", "r", encoding="utf-8"))
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
    sentence = ""

    for mot in mots_article:
        sentence += mot + " "
    # print("mots article : ", sentence)

    # Comparaison de chaque article dans l'annuaire avec chaque mot de l'article que l'on cherche à comparer
    for i, article in enumerate(annuaire):
        texte_entite = article["texte"]

        # score = nombre de mots de l'article qui sont dans l'entité
        for mot in mots_article:
            # score + 1 si le mot est dans l'article de l'annuaire
            if mot in texte_entite:
                scores[i] += 1

    # Trouver l'entité avec le score le plus élevé
    max_score = max(scores)

    # Si aucun score n'est supérieur à 0, il n'y a pas de correspondance
    if max_score == 0:
        return "none score = 0"

    # Trouver l'index de l'entité avec le score le plus élevé
    index_max = scores.index(max_score)
    resultat = annuaire[index_max]


    articles_score_max = []
    # si plusieurs articles ont le même score on utilise gpt3 pour les départager
    if scores.count(max_score) > 1:
        iter = 0

        # si plusieurs articles ont le même score, on les met dans la liste
        for i, article in enumerate(annuaire):
            if scores[i] == max_score:
                articles_score_max.append(article)
                # print(entite["texte"])
                iter += 1

        # on utilise gpt3 pour les départager
        resultat = gpt3_comparaison(sentence, articles_score_max)
        # on vérifie que gpt3 a pas inventé un article qui n'existe pas
        resultat = gestion_gpt3(resultat)

        # ça sert juste à afficher proprement le résultat pour l'analyse
        disp = ""
        # string mots_article
        for mot in mots_article:
            disp += mot + " "

        print(disp, "---> ", resultat["texte"], "max score : ", max_score, "gpt3", " i;", iter)

    # si un seul article a le score max, on le renvoie
    else:
        disp = ""
        # string mots_article
        for mot in mots_article:
            disp += mot + " "
        print(disp, "---> ", resultat["texte"], "max score : ", max_score)
    return resultat


def correspondance_liste(liste, annuaire):
    """
    Compare une liste json d'extraction avec l'annuaire pour trouver une correspondance pour chaque élément de la liste.
    :param liste: liste à comparer, liste de dicts avec clé 'name'
    :param annuaire: annuaire des articles, liste de dicts
    :return: liste des références des articles correspondants
    """
    liste_articles = []
    for article in liste:
        liste_articles.append(correspondance(article, annuaire))
    return liste_articles


def gestion_gpt3(nom_fourniture):
    """
    Fonction pour vérifier si le nom de l'article est dans l'annuaire, c'est fait pour vérifier si gpt3 a bien trouvé
    et a pas inventer un article qui n'existe pas
    """
    nom_fourniture = nom_fourniture.lower()
    # retrouver nom_fourniture dans annuaire
    for element in annuaire:
        if element["texte"].lower() == nom_fourniture:
            return element
    element["texte"] = "none"
    return element


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
    # tokens = [nlp(word)[0].lemma_ for word in tokens]
    # print(tokens)
    return tokens


annuaire = json.load(open("src/Matching/annuaire2.json", "r", encoding="utf-8"))
annuaire = annuaire["entities"]
