import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import base64
import requests

from main import main_process

app = Flask(__name__)
CORS(app)

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

@app.route('/use_opencv/<path:file_path>', methods=['GET'])
def test(file_path):
    print("Chemin du fichier :", file_path)
    # Logique pour traiter le fichier
    main_process(file_path)
    return jsonify({"file_path": file_path})


@app.route('/use_vertex/<path:file_path>', methods=['GET'])
def test_vertex(file_path):
    print("Chemin du fichier :", file_path)
    # Logique pour traiter le fichier
    # Mettre ici la fonction pour utiliser vertex
    return jsonify({"file_path": file_path})


@app.route('/use_gpt4/<path:file_path>', methods=['GET'])
def test_gpt4(file_path):
    print("Chemin du fichier :", file_path)
    # Logique pour traiter le fichier

    # Function to encode the image

    # Getting the base64 string
    base64_image = encode_image(file_path)


    # Mettre ici la fonction pour utiliser gpt4

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
            "text": "fais une liste de toutes les fournitures scolaire dans le texte suivant, sous forme [fourniture:nombre], donne moi que la liste en sortie:"
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
    "max_tokens": 500
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    content = response.json()['choices'][0]['message']['content']
    with open('recognized.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    
    return jsonify({"file_path": file_path})




@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Ici, vous pouvez enregistrer le fichier sur le serveur
    # récupérer l'extension du fichier
    extension = os.path.splitext(file.filename)[1]
    name = "file" + extension
    print("Chemin du fichier :", file.filename)
    file.save(os.path.join('uploads', secure_filename(name)))

    return jsonify({"message": "File uploaded successfully"}), 200


@app.route('/get-text')
def get_text():
    with open('recognized.txt', 'r', encoding='utf-8') as file:  # Assurez-vous d'utiliser l'encodage UTF-8
        content = file.read()
    return jsonify({"text": content}), 200, {'Content-Type': 'application/json; charset=utf-8'}


if __name__ == '__main__':
    app.run(debug=True)
