import os
import time
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from src.OCR.gpt4 import use_gpt4
from src.OCR.opencv_ocr import opencv_ocr
from src.Performance_and_evaluation.perf_measurement import compare_ocr
from src.OCR.vertex_ocr import vertex_ocr

app = Flask(__name__)
CORS(app)

@app.route('/use_opencv/<path:file_path>', methods=['GET'])
def test(file_path):
    start_time = time.time()
    print("Chemin du fichier :", file_path)
    # Logique pour traiter le fichier
    opencv_ocr(file_path)
    execution_time = time.time() - start_time
    return jsonify({"file_path": file_path, "execution_time": execution_time})


@app.route('/use_vertex/<path:file_path>', methods=['GET'])
def test_vertex(file_path):
    start_time = time.time()
    print("Chemin du fichier :", file_path)
    # Logique pour traiter le fichier
    vertex_ocr(file_path)
    execution_time = time.time() - start_time
    return jsonify({"file_path": file_path, "execution_time": execution_time})


@app.route('/use_gpt4/<path:file_path>', methods=['GET'])
def test_gpt4(file_path):
    start_time = time.time()
    use_gpt4(file_path)

    execution_time = time.time() - start_time
    
    return jsonify({"file_path": file_path, "execution_time": execution_time})


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
    file.save(os.path.join('../website/uploads', secure_filename(name)))

    return jsonify({"message": "File uploaded successfully"}), 200


@app.route('/get-text')
def get_text():
    with open('../recognized.txt', 'r', encoding='utf-8') as file:  # Assurez-vous d'utiliser l'encodage UTF-8
        content = file.read()
    return jsonify({"text": content}), 200, {'Content-Type': 'application/json; charset=utf-8'}


@app.route('/compare')
def compare():
    score = compare_ocr("data.txt", "recognized.txt")
    return jsonify({"score": score}), 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == '__main__':
    app.run(debug=True)
