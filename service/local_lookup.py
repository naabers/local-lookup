#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_cors import CORS
from eve import EveApi

app = Flask(__name__)
CORS(app)

@app.route("/characters/information/<character_names>")
def character_information_route(character_names):
    print(character_names)
    api = EveApi()

    character_names = character_names.split(",")
    characters = api.get_characters(character_names)

    character_losses = api.get_character_losses(characters)
    for character_id, character_loss_map in character_losses.items():
        for character in characters:
            if character.id == character_id:
                character.set_losses(character_loss_map)

    processed_data = []
    for character in characters:
        processed_data.append(character.get_info())

    return jsonify(processed_data)

if __name__ == "__main__":
    app.run()
