import json
import nltk
import spacy
from nltk.corpus import stopwords
import re

# Chargement du modèle français de SpaCy
nlp = spacy.load('fr_core_news_sm')

def preprocess_string(s):
    """
    Prétraitement d'un article "name" : "element", "nombre" : "element"
    :param s: string à prétraiter
    :return: string prétraitée
    """
    #remplacer les accents
    accent = {"é": "e", "è": "e", "ê": "e", "à": "a", "ç": "c", "ù": "u", "û": "u", "ô": "o", "î": "i", "ï": "i"}
    for key, value in accent.items():
        s = s.replace(key, value)
    #print(s)

    # remplacer les caractères spéciaux par des espaces
    tokens = re.sub(r"[^a-zA-Z0-9]", " ", s)
    #print(tokens)

    # tokenize
    tokens = nltk.word_tokenize(tokens, language='french')

    # supprimer les stopwords
    tokens = [word for word in tokens if word.lower() not in stopwords.words('french')]
    #print(tokens)

    # mettre en minuscule
    tokens = [word.lower() for word in tokens]
    #print(tokens)
    # lemmatization
    #tokens = [nlp(word)[0].lemma_ for word in tokens]
    #print(tokens)
    sentence = ""
    for word in tokens:
        sentence += word + " "

    return sentence


def preprocess_annuaire(annuaire):
    """
    Prétraite l'annuaire pour le rendre plus facile à comparer.
    :param annuaire: annuaire des articles, liste de dicts
    """
    for article in annuaire:
        article["texte"] = preprocess_string(article["texte"])
    return annuaire

print("preprocessing annuaire")
# use process_annuaire and save it
with open('src/Matching/annuaire.json', 'r', encoding='utf-8') as file:
    annuaire = json.load(file)
    annuaire = annuaire["entities"]
    annuaire = preprocess_annuaire(annuaire)
print("saving annuaire")

with open('src/Matching/annuaire3.json', 'w', encoding='utf-8') as f:
    json.dump(annuaire, f, ensure_ascii=False, indent=4)
print("done")

