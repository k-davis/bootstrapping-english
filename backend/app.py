from flask import Flask, jsonify
from flask.wrappers import Response
from flask_cors import CORS

from utils import disambiguate_synsets

app: Flask = Flask(__name__)
CORS(app)

@app.get("/wordsenses/<string:word>")
def get_synset(word: str) -> Response:
    disamb_synsets = disambiguate_synsets(word)
    return jsonify([s.to_dict() for s in disamb_synsets])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
