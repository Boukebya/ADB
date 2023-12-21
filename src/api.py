import os
import time
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from OCR.vertex_ocr import vertex_ocr
from Extraction.gpt3_extraction import gpt3_extraction
from Matching.levenschtein_matching import use_levenshtein
from waitress import serve


app = Flask(__name__)
CORS(app)


@app.route('/use_vertex/<path:file_path>/<classe>', methods=['GET'])
def vertex_request(file_path,classe):
    """
    Method to test OCR using Vertex, Extraction using GPT-3 and Matching using basic comparison and GPT-3
    :param file_path: path of the file to test
    :return: json with file_path, execution_time, content_ocr, result_extraction and matching
    """


    print("timer start")
    start_time = time.time()

    # OCR using Vertex
    vertex_ocr(file_path)

    # get text from ocr.txt
    with open('ocr.txt', 'r', encoding='utf-8') as file:
        content_ocr = file.read()
        print("done OCR")

    # Extraction using GPT3
    gpt3_extraction("ocr.txt", classe)
    with open('ocr.txt', 'r', encoding='utf-8') as file:
        content_extraction = file.read()
        print("done extraction")

    # Matching using basic comparison
    #gpt3_matching()
    use_levenshtein()
    with open('result.txt', 'r', encoding='utf-8') as file:
        matching = file.read()
    print("done matching")

    # return all texts
    execution_time = time.time() - start_time
    return jsonify({"file_path": file_path, "execution_time": execution_time , "content_ocr": content_ocr,
                    "result_extraction": content_extraction, "matching": matching})


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Method to upload a file on the server
    :return: json with message
    """

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
    file.save(os.path.join('src/website/uploads', secure_filename(name)))

    return jsonify({"message": "File uploaded successfully"}), 200


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
