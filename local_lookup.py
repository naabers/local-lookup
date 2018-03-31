#!/usr/bin/env python3

import requests
from flask import Flask, jsonify
from xml.etree import ElementTree
app = Flask(__name__, static_url_path='')

"""
Items:
cyno:        21096
covert cyno: 28646

"""

def is_scary_item(item_type_id):
    if item_type_id == 21096:
        return True
    elif item_type_id == 28646:
        return True
    return False

def get_scary_item_name(item_type_id):
    if item_type_id == 21096:
        return "cyno"
    elif item_type_id == 28646:
        return "covert cyno"
    return ""

def get_character_ids(character_names):
    character_id_map = {}
    character_name_csv = ",".join(character_names)

    url = "https://api.eveonline.com/eve/CharacterID.xml.aspx?names=" + character_name_csv
    search_results = requests.get(url)
    root = ElementTree.fromstring(search_results.content)
    rowset = root.find('.//rowset[@name="characters"]')
    for row in rowset.findall("row"):
        character_name = row.get('name')
        character_id = int(row.get('characterID'))
        character_id_map[character_id] = character_name
    return character_id_map

def get_character_losses(character_id_map):
    #take the keys for the dictionary as a list
    character_ids = list(character_id_map)
    #zkillboard requires the ids to be sorted for its api
    character_ids.sort()
    character_id_str = ",".join(str(i) for i in character_ids)
    url = "https://zkillboard.com/api/losses/characterID/" + character_id_str + "/"
    headers = {'Accept-Encoding': 'gzip', 'User-Agent': 'naabers'}
    search_results = requests.get(url, headers=headers)

    return search_results.json()

def get_ship_name(ship_type_id):
    url = "https://esi.tech.ccp.is/latest/universe/types/" + ship_type_id + "/"
    search_results = requests.get(url)

    return search_results.json()["name"]

def process_character_losses(character_id_map, character_losses):
    processed_data = []
    for killmail in character_losses:
        victim = killmail["victim"]
        for item in victim["items"]:
            item_type_id = item["item_type_id"]
            if is_scary_item(item_type_id):
                processed_data.append(process_loss_info(character_id_map, killmail, item_type_id))
                break
    return processed_data

def process_loss_info(character_id_map, killmail, item_type_id):
    processed_loss = {}
    victim = killmail["victim"]

    processed_loss['character_name'] = character_id_map[victim["character_id"]]
    processed_loss['killmail_time'] = killmail["killmail_time"]
    processed_loss['ship_name'] = get_ship_name(str(victim["ship_type_id"]))
    processed_loss['item_discovered'] = get_scary_item_name(item_type_id)

    return processed_loss

@app.route("/characters/information/<character_names>")
def character_information_route(character_names):
    character_names = character_names.split(",")
    character_id_map = get_character_ids(character_names)
    character_losses = get_character_losses(character_id_map)
    processed_data = process_character_losses(character_id_map, character_losses)

    return jsonify(processed_data)

@app.route('/lookup')
def root():
    return app.send_static_file('lookup.html')

if __name__ == "__main__":
    app.run()
