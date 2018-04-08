from .cache import cache

import requests

@cache()
def get_ship_name(ship_type_id):
    url = "https://esi.tech.ccp.is/latest/universe/types/" + str(ship_type_id) + "/"
    search_results = requests.get(url)

    return search_results.json()["name"]


@cache()
#takes in a list of character names
#returns a map of character id to name
def get_character_ids(character_names):
    character_id_map = {}
    url = "https://esi.tech.ccp.is/latest/universe/ids/"
    search_results = requests.post(url, json = character_names)
    json_results = search_results.json()
    character_results = json_results["characters"]

    for character in character_results:
        character_name = character["name"]
        character_id = character["id"]
        character_id_map[character_id] = character_name

    return character_id_map
