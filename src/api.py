import os
import time
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from OCR.gpt4 import use_gpt4
from Performance_and_evaluation.perf_measurement import compare_ocr
from OCR.vertex_ocr import vertex_ocr
from Extraction.gpt3_extraction import gpt3_extraction
from Matching.basic_comparison import gpt3_matching
from Matching.levenschtein_matching import use_levenshtein

app = Flask(__name__)
CORS(app)


@app.route('/use_opencv/<path:file_path>', methods=['GET'])
def opencv_request(file_path):
    """
    Method to test OCR using OpenCV
    :param file_path: path of the file to test
    :return: json with file_path and execution_time
    """
    start_time = time.time()

    print("Localisation du script :", os.path.dirname(os.path.realpath(__file__)) + "/api.py")
    print("Chemin du fichier :", file_path)

    # Method to do OCR using OpenCV, result is saved in ocr.txt
    #opencv_ocr(file_path)

    execution_time = time.time() - start_time
    return jsonify({"file_path": file_path, "execution_time": execution_time})


@app.route('/use_vertex/<path:file_path>', methods=['GET'])
def vertex_request(file_path):
    """
    Method to test OCR using Vertex, Extraction using GPT-3 and Matching using basic comparison and GPT-3
    :param file_path: path of the file to test
    :return: json with file_path, execution_time, content_ocr, result_extraction and matching
    """

    classe = ""
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


@app.route('/use_gpt4/<path:file_path>', methods=['GET'])
def gpt4_request(file_path):
    """
    Method to test OCR, Extraction and Matching using GPT-4
    :param file_path: path of the file to test
    """

    start_time = time.time()
    # Method to do OCR, Extraction and Matching using GPT-4
    use_gpt4(file_path)

    execution_time = time.time() - start_time
    return jsonify({"file_path": file_path, "execution_time": execution_time})


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

# not used
@app.route('/get-text')
def get_text():
    with open('ocr.txt', 'r', encoding='utf-8') as file:  # Assurez-vous d'utiliser l'encodage UTF-8
        content = file.read()
    return jsonify({"text": content}), 200, {'Content-Type': 'application/json; charset=utf-8'}

# not used
@app.route('/compare')
def compare():
    score = compare_ocr("Furniture_list/data_1.txt", "ocr.txt")
    return jsonify({"score": score}), 200, {'Content-Type': 'application/json; charset=utf-8'}


if __name__ == '__main__':
    app.run(debug=True)
