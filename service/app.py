from flask import Flask, jsonify
from flask_cors import CORS

from local_lookup import local_lookup

app = Flask(__name__)
CORS(app)


@app.route("/characters/information/<character_names>")
def character_information_route(character_names):
    processed_data = local_lookup.get_character_information(character_names)
    return jsonify(processed_data)


if __name__ == "__main__":
    app.run()