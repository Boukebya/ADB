from openai import OpenAI
import time


def gpt3_extraction(file_path):
    """
    Use GPT-3 to extract the list of school supplies from a text file.
    Extraction is then done.
    :param file_path: path to the text file
    """

    start_time = time.time()
    api_key = "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"
    client = OpenAI(api_key=api_key)
    with open(file_path, "rb") as text_file:
        file = text_file.read().decode('utf-8')

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        temperature=0.2,
        messages=[
            {"role": "system",
             "content": "Vous êtes un assistant utile conçu pour extraire des fournitures scolaires du texte sans omission."},
            {"role": "user", "content": """fais une liste de toutes les fournitures
             scolaire dans le texte suivant sous forme :
             {
             "name": "nom de l'article avec ses détails",
             "nombre": 1 
             },
              name correspond au nom du produit que tu as trouvé, avec ses dimensions et poids si disponible uniquement,
              J'inste sur le uniquement, ne met pas de détail inutile, le but et de retrouver la fourniture scolaire
              dans une base de données d'articles après, garde donc les détails essentiels à cette tâche.
              Les fournitures que tu vas retrouvés vont être comparés à une liste dont les éléments ressemble à cela:
              "texte": "cahier texte reliure integrale 124 pages format 17x22 cm reglure seyes papier blanc 70g",
              garde donc les détails similaire.
              number correspond au nombre d'articles a acheter dans la liste, si ce n'est pas indique met 1 par défaut.
              Fais bien attention à ne pas surinterpréter le texte.
              Aussi, fais attention dans le cas ou il y'a le même nom d'articles en couleur différente,
              créé un article pour chaque couleur. 
              ne donne que le contenu en json, pas de texte en plus, n'oublie pas les [ et ] au début et a la fin du json.
            """ + file}
        ]
    )
    print(response.choices[0].message.content)
    print(response.usage)
    #print("%s seconds to achieve extraction" % (time.time() - start_time))

    with open('ocr.txt', 'w', encoding='utf-8') as f:
        f.write(response.choices[0].message.content)


def gpt3_comparaison(fourniture, liste):
    """
    Use GPT-3 to extract the list of school supplies from a text file.
    Extraction is then done.
    :param file_path: path to the text file
    """

    truc = "J'ai cette fourniture scolaire :"
    truc += fourniture
    truc += ", il faut que tu l'associes à la fourniture scolaire qui a le plus de chance de correspondre dans le texte qui va suivre," \
            " si tu ne trouves pas de correspondance entre l'article et les éléments de la liste, renvoie none, j'attends en retour un des articles suivants uniquement, sans texte en plus:\n"
    for element in liste:
        truc += element["texte"]
        truc += "\n"

    #print(truc)
    start_time = time.time()
    api_key = "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"
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        temperature=0.4,
        messages=[
            {"role": "system",
             "content": "Vous êtes un assistant utile conçu pour associer des fournitures scolaires du texte sans omission, fournis uniquement en sortie l'article qui correspond le plus à la fourniture scolaire donnée."},
            {"role": "user", "content": truc}
        ]
    )
    #print("%s seconds to achieve extraction" % (time.time() - start_time))
    #print(response.usage)
    return response.choices[0].message.content
#gpt3_extraction("../ocr.txt")
