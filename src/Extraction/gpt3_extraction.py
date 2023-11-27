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
        messages=[
            {"role": "system",
             "content": "Vous êtes un assistant utile conçu pour extraire des fournitures scolaires du texte sans omission."},
            {"role": "user", "content": """fais une liste de toutes les fournitures
             scolaire dans le texte suivant sous forme produit:nombre, il faut faire une ligne par couleur pour les produits
             similaire , le nombre doit être un entier qui vaut 1 par défaut, et correspond aux nombres d'articles sur la liste,
             donne moi uniquement la liste en sortie en format : (
             {
  "name": "", contient le nom du produit avec le format le poids la marque la couleur la taille dans une seul string sans virgule
  "nombre": "", contient le nombre d'articles de ce produit à acheter, attention dans le cas d'un produit avec plusieurs couleurs,
  s'il est écrit 4 stylo, bleu vert rouge et bleu, la somme est de 4 donc chaque nombre sera à 1
}
)
            """ + file}
        ]
    )
    print(response.choices[0].message.content)
    print(response.usage)
    #print("%s seconds to achieve extraction" % (time.time() - start_time))

    with open('ocr.txt', 'w', encoding='utf-8') as f:
        f.write(response.choices[0].message.content)


#gpt3_extraction("../ocr.txt")
