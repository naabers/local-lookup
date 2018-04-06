#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_cors import CORS

import character
import eve
import zkill

app = Flask(__name__)
CORS(app)

def process_killmails(characters, killmails):
    character_map = {}
    for character_obj in characters:
        character_map[character_obj.id] = character_obj

    for killmail in killmails:
        if killmail.victim_id in character_map:
            character_map[killmail.victim_id].losses.append(killmail)
        else:
            for attacker_id in killmail.attackers:
                if attacker_id in character_map:
                    character_map[attacker_id].kills.append(killmail)

@app.route("/characters/information/<character_names>")
def character_information_route(character_names):
    print(character_names)

    character_names = character_names.split(",")
    character_name_map = eve.get_characters(character_names)

    characters = []
    for character_name, character_id in character_name_map.items():
        character_obj = character.Character(character_id, character_name)
        characters.append(character_obj)

    # killmails = zkill.get_character_losses(characters)
    killmails = zkill.get_character_kills_and_losses(characters)
    process_killmails(characters, killmails)

    processed_data = []
    for character_obj in characters:
        processed_data.append(character_obj.get_info())

    return jsonify(processed_data)

if __name__ == "__main__":
    app.run()
