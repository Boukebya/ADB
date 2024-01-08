import json
from openai import OpenAI

with open('src/config.json', 'r') as config_file:
    config = json.load(config_file)

google_var = config['google_cloud']

openai_var = config['openai']
open_ai_key = openai_var['api_key']


def gpt3_extraction(file_path, classe):
    """
    Use GPT-3 to extract the list of school supplies from the OCR text file.
    Extraction is then done in the file ocr.txt.
    :param file_path: path to the text file
    """

    client = OpenAI(api_key=open_ai_key)
    with open(file_path, "rb") as text_file:
        file = text_file.read().decode('utf-8')

    msg = """fais une liste des fournitures scolaires écrit au singulier, article par article, individuellement,"""

    # if string contains more than 1 character :
    if len(classe) > 1:
        msg += """ pour la classe de : """
        msg += classe
        print(msg)

    msg += """, pas d'habits ou d'affaires de sport, dans le texte suivant sous forme :
             {
             "name": "nom d'un seul article avec ses détails, dimensions, poids, etc. si disponible,",
             "article": "Mot correspondant le plus à l'article,sans détails,",
             "nombre": 1, par défaut, si non indiqué
             },
              name correspond au nom du produit que tu as trouvé,
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
        temperature=0,
        messages=[
            {"role": "system",
             "content": "Vous êtes un assistant utile conçu pour extraire des fournitures scolaires du texte"
                        " sans omission, tu mets les fournitures au singulier"},
            {"role": "user", "content": msg + file}
        ]
    )
    print(response.choices[0].message.content)
    print(response.usage)

    with open('ocr.txt', 'w', encoding='utf-8') as f:
        f.write(response.choices[0].message.content)