import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import spacy

print(spacy.info())
chemin_modele = r'C:\Users\Yanis\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\site-packages\fr_core_news_sm\fr_core_news_sm-3.7.0'

nlp = spacy.load(chemin_modele)
def preprocess_article_name(name):
    # Conversion en minuscules
    name = name.lower()
    nlp = spacy.load("fr_core_news_sm")
    # Remplacement des accents
    accents = {
        "àâä": "a", "éèêë": "e", "îï": "i",
        "ôö": "o", "ùûü": "u", "ç": "c"
    }
    for accented_chars, replacement in accents.items():
        name = re.sub(f"[{accented_chars}]", replacement, name)

    # Suppression des caractères spéciaux
    name = re.sub(r"[^a-zA-Z0-9 ]+", ' ', name)

    # Tokenisation
    tokens = word_tokenize(name, language='french')

    # Filtrage des stop words
    tokens = [word for word in tokens if word.lower() not in stopwords.words('french')]

    # Lemmatisation avec spaCy
    doc = nlp(' '.join(tokens))
    lemmatized_tokens = [token.lemma_ for token in doc]

    return lemmatized_tokens

# Fonction pour comparer les articles
def correspondance(article, annuaire):
    """
    Compare l'article avec l'annuaire pour trouver une correspondance.
    :param article: article à comparer, dict avec clé 'name'
    :param annuaire: annuaire des articles, liste de dicts avec clés 'texte' et 'type'
    :return: référence de l'article correspondant avec le plus haut score
    """
    # Initialisation des scores pour chaque entité de l'annuaire
    scores = [0] * len(annuaire)

    filtered = preprocess_article_name(article["name"])

    mots_article = filtered
    #print(mots_article)

    # Comparaison de chaque mot de l'article avec chaque entité de l'annuaire
    for i, entite in enumerate(annuaire):
        texte_entite = entite["texte"]
        # remove capital letters
        texte_entite = texte_entite.lower()


        for mot in mots_article:
            if mot in texte_entite:
                scores[i] += 1

    # Trouver l'entité avec le score le plus élevé
    max_score = max(scores)
    index_max = scores.index(max_score)
    entite_correspondante = annuaire[index_max]
    print(article["name"],"Max obtenu : ", max_score, "pour : ", entite_correspondante["texte"])
    return entite_correspondante

def correspondance_liste(liste, annuaire) :
    """
    Compare une liste json avec l'annuaire pour trouver une correspondance pour chaque élément de la liste.
    :param liste: liste à comparer, liste de dicts avec clé 'name'
    :param annuaire: annuaire des articles, liste de dicts
    """
    for article in liste:
        correspondance(article, annuaire)


annuaire = json.load(open("annuaire.json", "r", encoding="utf-8"))
annuaire = annuaire["fournitures"]
annuaire = annuaire["entities"]

mes_articles = json.load(open("../Furniture_list/data_extraction_1.json", "r", encoding="utf-8"))

correspondance_liste(mes_articles, annuaire)
