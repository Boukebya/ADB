from openai import OpenAI


def gpt3_extraction(file_path, classe):
    """
    Use GPT-3 to extract the list of school supplies from the OCR text file.
    Extraction is then done in the file ocr.txt.
    :param file_path: path to the text file
    """

    api_key = "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"
    client = OpenAI(api_key=api_key)
    with open(file_path, "rb") as text_file:
        file = text_file.read().decode('utf-8')

    msg = """fais une liste de toutes les fournitures scolaire"""

    if classe != "":
        msg += """pour la classe """
        msg += classe

    msg += """, pas d'habits ou d'affaires de sport, dans le texte suivant sous forme :
             {
             "name": "nom de l'article avec ses détails",
             "article": "nom de l'article le plus important sans détails",
             "nombre": 1 
             },
              name correspond au nom du produit que tu as trouvé au singulier, j'insiste, mets les articles au singulier,
              par exemple, gommes -> gomme, cahiers -> cahier, stylos -> stylo, etc.
              avec ses dimensions et poids si disponible, et autres informations, 
              si la dimension pour le cahier n'est pas disponible, mets
              24x32 cm par défaut. S'il est écrit grand format, mets 24x32 cm, si c'est petit format, mets 17x22 cm.
              J'insiste sur le uniquement, ne met pas de détail inutile, le but et de retrouver la fourniture scolaire
              dans une base de données d'articles après, garde donc les détails essentiels à cette tâche.
              Ne mets pas le nombre d'articles à acheter dans name. Aussi, rajoute des synonymes, par exemple,
              fluo, ou scotch, rajoute des synonymes tel que surligneur, ou ruban adhésif ou rouleau pour tous les articles.
              Vraiment, rajoute des synonymes quand le mot est trop vague comme scotch ou fluo, c'est nécessaire.
              Les fournitures que tu vas retrouvés vont être comparés à une liste dont les éléments ressemble à cela:
              "name": "cahier texte reliure integrale 124 pages format 17x22 cm reglure seyes papier blanc 70g",
              garde donc les détails similaire. Si possible, après cela, rajoute des synonymes du mot le plus important
                de l'article, par exemple, scotch -> ruban adhésif, porte vues -> protège document, etc.
              "article" correspond au nom de l'article le plus important, sans détails, crayon de bois -> crayon,
                cahier de texte -> cahier, pochette à élastique -> pochette à élastique, etc... 
                Le but est de garder l'information importante
              nombre correspond au nombre d'articles a acheter dans la liste, si ce n'est pas indique met 1 par défaut.
              Fais bien attention à ne pas surinterpréter le texte.
              Aussi, fais attention dans le cas ou il y'a le même nom d'articles en couleur différente, par exemple,
              cahier 24x32 rouge, bleu, vert, ou stylo bleu, rouge, vert, etc. Dans ce cas-là, il faut que tu
              créé une entité pour chaque couleur, N'oublie pas de mettre les noms au singulier dans ce cas-là.
              ne donne que le contenu en json, pas de texte en plus, n'oublie pas les [ et ] au début et a la fin du json.
            """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        temperature=0.3,
        messages=[
            {"role": "system",
             "content": "Vous êtes un assistant utile conçu pour extraire des fournitures scolaires du texte"
                        " sans omission. Tu écris aux singulier les articles."},
            {"role": "user", "content": msg + file}
        ]
    )
    print(response.choices[0].message.content)
    print(response.usage)

    with open('ocr.txt', 'w', encoding='utf-8') as f:
        f.write(response.choices[0].message.content)


def gpt3_comparaison(fourniture, liste):
    """
    Use GPT-3 to find the most similar school supply in the list.
    :param fourniture: school supply to find
    :param liste: list of school supplies to compare
    """

    text_input = "J'ai cette fourniture scolaire :"
    text_input += fourniture
    text_input += ", il faut que tu l'associes à la fourniture scolaire qui a le plus de chance de correspondre dans le texte qui va suivre," \
            " si tu ne trouves pas de correspondance entre l'article et les éléments de la liste," \
            "par exemple, sac de sport ne correspond pas avec sachet 100 pochettes renvoie none," \
            " j'attends en retour un des articles suivants uniquement, sans texte en plus:\n"

    for element in liste:
        text_input += element["texte"]
        text_input += "\n"

    api_key = "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"
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        temperature=0.1,
        messages=[
            {"role": "system",
             "content": "Vous êtes un assistant utile conçu pour associer des fournitures scolaires du texte"
                        " sans omission, fournis uniquement en sortie l'article qui correspond le plus"
                        " à la fourniture scolaire donnée."},
            {"role": "user", "content": text_input}
        ]
    )
    #print(response.usage)
    return response.choices[0].message.content