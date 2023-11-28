import base64
import requests
import json

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def use_gpt4(file_path):
    print("Chemin du fichier :", file_path)
    # Logique pour traiter le fichier

    # Function to encode the image

    # Getting the base64 string
    base64_image = encode_image(file_path)

    # OpenAI API Key
    api_key = "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"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    annuaire = json.load(open("Matching/annuaire.json", "r", encoding="utf-8"))
    annuaire_str = json.dumps(annuaire)

    payload = {
        "model": "gpt-4-vision-preview",
        "temperature": 0,  # Valeur faible pour moins d'interprétation
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Je t'ai fourni une liste scolaire, il faut que tu l'analyse et en extrais tous les éléments correspondanr à des fournitures scolaires, extraits chaque éléments et associe chacun des articles extraits avec l'élément de cette annuaire qui a le plus de correspondance: https://drive.google.com/file/d/1UIxqO0-kBwAN5A9mL3w7vzdJs6SRwWc6/view?usp=sharing"

                                ,
                        #"text": "Extrais moi tout le texte de l'image suivante, sans faire d'erreur et en gardant la mise en page, n'oublie aucun mot et garde absolument tout le contenu:"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 2000,
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    content = response.json()['choices'][0]['message']['content']
    with open('ocr.txt', 'w', encoding='utf-8') as f:
        f.write(content)
