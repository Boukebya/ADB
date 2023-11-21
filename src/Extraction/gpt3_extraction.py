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
             "content": "Vous êtes un assistant utile conçu pour extraire des fournitures scolaires du texte."},
            {"role": "user", "content": """fais une liste de toutes les fournitures scolaire dans le texte suivant sous forme produit:nombre, si plusieurs couleurs pour le produit faire un élement par produit, le nombre doit être un entier qui vaut 1 par défaut, met encre avec couleur si besoin en tant qu'objet à part, donne moi que la liste en sortie:
   """ + file}
        ]
    )
    print(response.choices[0].message.content)
    print(response.usage)
    #print("%s seconds to achieve extraction" % (time.time() - start_time))

    with open('ocr.txt', 'w', encoding='utf-8') as f:
        f.write(response.choices[0].message.content)


#gpt3_extraction("../ocr.txt")
