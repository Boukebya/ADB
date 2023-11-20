import base64
import requests


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
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        #             "text": "fais une liste de toutes les fournitures scolaire dans le texte suivant, sous forme [fourniture:nombre], donne moi que la liste en sortie:"
                        "text": "Extrais moi tout le texte de l'image suivante, sans faire d'erreur et en gardant la mise en page, n'oublie aucun mot et garde absolument tout le contenu:"
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
        "max_tokens": 800
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    content = response.json()['choices'][0]['message']['content']
    with open('recognized.txt', 'w', encoding='utf-8') as f:
        f.write(content)
