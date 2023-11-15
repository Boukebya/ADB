import os

from flask import Flask, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename

from prototype.main import main_process

app = Flask(__name__)


@app.route('/use/<path:file_path>', methods=['GET'])
def test(file_path):
    print("Chemin du fichier :", file_path)
    # Logique pour traiter le fichier
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



if __name__ == '__main__':
   app.run(debug = True)