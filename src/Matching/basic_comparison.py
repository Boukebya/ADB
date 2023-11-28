import json

# Votre article
mon_article = {
    "name": "pochette à élastiques et rabats (format A4)",
    "nombre": 1
}


# Fonction pour comparer les articles
def correspondance(article, annuaire):
    """
    Compare l'article avec l'annuaire pour trouver une correspondance
    :param article: article à comparer
    :param annuaire: annuaire des articles
    :return: article correspondant
    """
    annuaire_test = annuaire.copy()
    score = {key: 0 for key in annuaire_test.keys()}
    for word in article["name"].split():
        print(word)
        #compare each word with each word in the dictionary and add 1 to the score if it matches the element of dictionnary
        for key in annuaire_test.keys():
            if word in key:
                score[key] += 1
                print(score)


    return score


annuaire = json.load(open("annuaire.json", encoding="utf-8"))

# Trouver la correspondance
resultat = correspondance(mon_article, annuaire)

# Afficher le résultat
if resultat:
    print(resultat)
else:
    print("Aucune correspondance trouvée")
