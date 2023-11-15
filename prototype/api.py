import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS

from prototype.main import main_process

app = Flask(__name__)
CORS(app)


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
    # Mettre ici la fonction pour utiliser gpt4
    main_process(file_path)
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
