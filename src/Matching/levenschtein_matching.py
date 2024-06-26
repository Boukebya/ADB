import re
import nltk
from fuzzywuzzy import fuzz
import json
from nltk.corpus import stopwords
from Matching.special_case import match_book, match_paper
nltk.download('punkt')
nltk.download('stopwords')

def best_match_levenshtein(str, annuaire):
    """
    Renvoie l'article de l'annuaire qui correspond le mieux à l'article donné.
    Renvoie rien si aucun article ne correspond, et renvoie un article aléatoire si plusieurs articles ont le même score.
    :param str: article à comparer, dict avec clé 'name'
    :param annuaire: annuaire des articles, liste de dicts avec clés 'texte' et 'type'
    :return: reference de l'article correspondant avec le plus haut score
    """
    # if annuaire is only one article
    if type(annuaire) == dict:
        texte = annuaire["texte"]
        # if annuaire["nombre exist
        if "nombre" in annuaire:
            nb = annuaire["nombre"]

        with open('test.txt', 'a', encoding='utf-8') as file:
            write = str["name"] + " --> " + texte + " " + "\n"
            file.write(write)
        return annuaire

    # if annuaire is nonetype
    if annuaire == None:
        with open('test.txt', 'a', encoding='utf-8') as file:
            file.write(str["name"] + " --> " + "annuaire vide" + "\n")
        print(str["name"], " --> ", "article non trouvé dans best match ")
        return {"texte": "article score inferieur à 0 ", "reference": "none"}

    scores = []
    for article in annuaire:
        scores.append(fuzz.partial_ratio(str["name"], article["texte"]))
    max_score = max(scores)
    # print(max_score)

    # return a random article with max score
    for i, article in enumerate(annuaire):
        if scores[i] == max_score and max_score > 30:
            with open('test.txt', 'a', encoding='utf-8') as file:
                write = str["name"] + " --> " + article["texte"] + "\n"
                file.write(write)

            print(str["name"], " --> ", article["texte"], " : ", max_score)
            return article


    return {"texte": "article non trouvé levenschtein", "reference": "none"}


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


def format_to_catalog(article):
    """
    formatte le texte pour correspondre à l'annuaire, remplace les mots par des formulations présentes dans l'annuaire,
    au cas par cas
    :param s: string à formatter
    :return: string formatée
    """
    s = article["name"]

    s = s.lower()
    s = s.replace("grand cahier", "cahier 24x32")
    s = s.replace("feuilles doubles", "feuilles doubles copies doubles")
    s = s.replace("pochette plastifiee", "protege document")
    s = s.replace("pochettes plastifiees", "protege document")
    s = s.replace("porte vues", "protege document")
    # if a4 is pre, add 21x29
    s = s.replace("pochette cartonnée", "chemise")
    # if s = chemise, or protege document replace article["article"] by chemise or protege document
    if "chemise" in s:
        article["article"] = "chemise"
    if "protege document" in s:
        article["article"] = "protege document"
    if "a4" in s:
        s += " 21x29"
    return article


def correspondance_score(article, catalog):
    """
    Compare l'article avec l'annuaire pour trouver une correspondance, fonctionne avec un système de score.
    Le système de score est le suivant:
    -1 si le mot important n'est pas dans l'article de l'annuaire
    +4 si le mot important est dans l'article de l'annuaire
    +10 pour les ref spécifiques
    +1 si un mot de l'article est dans l'article de l'annuaire
    :param article: article à comparer, dict avec clé 'name'
    :param catalog: annuaire des articles, liste de dicts avec clés 'texte' et 'type'
    :return: reference de l'article correspondant avec le plus haut score, ou liste d'articles si plusieurs articles ont
    le même score
    """

    # Initialisation des scores pour chaque entité de l'annuaire
    scores = [0] * len(catalog)

    # Prétraitement de l'article
    article = format_to_catalog(article)
    article = format_to_catalog(article)
    nombre = article["nombre"]
    nombre = str(nombre)

    mots_article = preprocess_string(article["name"])
    important_word = preprocess_string(article["article"])
    sentence_article = ""
    sentence_important_word = ""

    for mot in mots_article:
        sentence_article += mot + " "

    for mot in important_word:
        sentence_important_word += mot + " "

    #print(sentence)
    #print(imp_word)

    # si l'article est un cahier, on utilise le matching spécial

    if "cahier" in sentence_article:
        result = match_book(sentence_article)
        print("find using book matching")
        if result != None:
            # add nombre to result
            result["nombre"] = nombre
        return result
    if "feuille" in sentence_article or "papier" in sentence_article or "ramette" in sentence_article or "ramettes" in sentence_article or "feuilles" in sentence_article:
        words = ["crayon", "crayons", "stylo", "stylos", "calque", "milimetree", "carton","milimetre"]
        if all(word not in sentence_article for word in words):
            # Votre logique ici
            print("find using paper matching ", sentence_article)
            result = match_paper(sentence_article)
            if result != None:
                # add nombre to result
                result["nombre"] = nombre
            return result

    # Comparaison de chaque article dans l'annuaire avec chaque mot de l'article que l'on cherche à comparer
    for i, article_catalog in enumerate(catalog):
        texte_article_catalog = article_catalog["texte"]

        if sentence_important_word in texte_article_catalog:
            scores[i] += 4
        else:
            scores[i] -= 1

        if "agenda" in sentence_article and article_catalog["reference"] == "30456":
            scores[i] += 10
        if "crayon de bois" in sentence_article and article_catalog["reference"] == "78567U12":
            scores[i] += 10
        if "stylo plume" in sentence_article and article_catalog["reference"] == "27511":
            scores[i] += 10
        if "crayons de couleurs" in sentence_article and article_catalog["reference"] == "20294":
            scores[i] += 10
        if "cle usb" in sentence_article and article_catalog["reference"] == "72822":
            scores[i] += 10
        if "correcteur" in sentence_article and article_catalog["reference"] == "34848":
            scores[i] += 10
        if "papier calque" in sentence_article and article_catalog["reference"] == "43007":
            scores[i] += 10
        if "regle" in sentence_article and article_catalog["reference"] == "78324":
            scores[i] += 10
        if "taille crayon" in sentence_article and article_catalog["reference"] == "7520":
            scores[i] += 10
        if "equerre" in sentence_article and article_catalog["reference"] == "79844":
            scores[i] += 10
        if "rapporteur" in sentence_article and article_catalog["reference"] == "79847":
            scores[i] += 10
        if "compas" in sentence_article and article_catalog["reference"] == "60825":
            scores[i] += 10
        if "gomme" in sentence_article and article_catalog["reference"] == "35329":
            scores[i] += 10


        # Les conditions spéciales pour "feuilles" et "protege cahier"
        if ("feuilles" in sentence_article and "protege cahier" in texte_article_catalog) or \
                ("protege" in sentence_article and "cahier" in texte_article_catalog):
            scores[i] -= 10
        if ("crayon" in sentence_article and "couleur" in sentence_article) and "crayon" in texte_article_catalog and "couleur" in texte_article_catalog:
            scores[i] += 10
        if ("feutre" in sentence_article and "couleur" in sentence_article) and "feutre" in texte_article_catalog and "couleur" not in texte_article_catalog:
            scores[i] += 10

        # score = nombre de mots de l'article qui sont dans l'entité
        for mot in mots_article:
            # score + 1 si le mot est dans l'article de l'annuaire

            if mot in texte_article_catalog:
                scores[i] += 1

    # Trouver l'entité avec le score le plus élevé
    max_score = max(scores)
    # print(max_score)


    # Si aucun score n'est supérieur à 0, il n'y a pas de correspondance
    if max_score <= 0:
        with open('test.txt', 'a', encoding='utf-8') as file:
            file.write(sentence_article + " --> " + "Aucun score > 0 dans le basic matching" + "\n")
        print(sentence_article, " --> ", "Aucun score > 0 dans le basic matching")
        out = {"texte": "Aucun score > 0 ", "reference": "none"}
        return out



    articles_score_max = []
    # si plusieurs articles ont le même score
    if scores.count(max_score) >= 1:
        iter = 0

        # si plusieurs articles ont le même score, on les met dans la liste
        for i, article in enumerate(catalog):
            if scores[i] == max_score:
                articles_score_max.append(article)

                # print(entite["texte"])
                iter += 1

        for article in articles_score_max:
            article["nombre"] = nombre

        return articles_score_max


def correspondance_list_article(content_extraction, annuaire):
    """
    Compare une liste json d'extraction avec l'annuaire pour trouver une correspondance pour chaque élément de la liste.
    :param liste: liste à comparer, liste de dicts avec clé 'name'
    :param annuaire: annuaire des articles, liste de dicts
    :return: liste des references des articles correspondants
    """
    listes_pre = []
    liste_articles = []

    for article in content_extraction:
        liste_articles.append(correspondance_score(article, annuaire))

    i = 0
    for article in content_extraction:
        listes_pre.append(best_match_levenshtein(article, liste_articles[i]))
        i += 1

    return listes_pre


def use_levenshtein():
    """
    Fonction pour faire le matching à partir d'un fichier ocr.txt, et écrire le résultat dans un fichier test.txt
    """
    # if test.txt exists, delete it, else create it
    try:
        with open('test.txt', 'w', encoding='utf-8') as file:
            file.write("")
    except:
        with open('test.txt', 'x', encoding='utf-8') as file:
            file.write("")

    with open('ocr.txt', 'r', encoding='utf-8') as file:
        content_ocr = file.read()
    # if content_ocr first line is ```json, remove it, happens with GPT-3
    if content_ocr[0] == "`":
        content_ocr = content_ocr.split("\n")
        content_ocr = content_ocr[1:-1]
        content_ocr = "\n".join(content_ocr)

    # read content_ocr as json
    content_extraction = json.loads(content_ocr)

    with open('src/Matching/annuaire3.json') as json_file:
        annuaire = json.load(json_file)

    listes_articles = correspondance_list_article(content_extraction, annuaire)

    # write file "result.txt" with all articles
    with open('result.txt', 'w', encoding='utf-8') as file:
        for article in listes_articles:
            if article != {"texte": "article non trouvé"}:
                # write article as a json
                json.dump(article, file, ensure_ascii=False)
                file.write("\n")

            else:
                file.write(article["texte"], " --> Article non trouvé")
                file.write("\n")

#use_levenshtein()