from flask import Flask, request, jsonify, redirect, url_for
from prototype.main import main_process

app = Flask(__name__)


@app.route('/use/<path>', methods=['GET'])
def test(path):
    print("truc ici:" + path)
    # retirer les " au début et à la fin
    path = path[1:-1]

    main_process(path)
    return path


if __name__ == '__main__':
   app.run(debug = True)