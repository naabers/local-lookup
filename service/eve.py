from xml.etree import ElementTree
import requests

SHIP_ID_TO_NAME_DICT = {}

#takes in a list of character names
#returns a map of character name to id
def get_characters(character_names):
    characters = {}
    character_name_csv = ",".join(character_names)
    url = "https://api.eveonline.com/eve/CharacterID.xml.aspx?names=" + character_name_csv
    print(url)
    search_results = requests.get(url, timeout=20)
    print("finished request")
    root = ElementTree.fromstring(search_results.content)
    rowset = root.find('.//rowset[@name="characters"]')
    for row in rowset.findall("row"):
        character_name = row.get('name')
        character_id = int(row.get('characterID'))
        characters[character_name] = character_id
    return characters

def get_ship_name(ship_type_id):
    global SHIP_ID_TO_NAME_DICT
    if ship_type_id in SHIP_ID_TO_NAME_DICT:
        return SHIP_ID_TO_NAME_DICT[ship_type_id]
    url = "https://esi.tech.ccp.is/latest/universe/types/" + str(ship_type_id) + "/"
    search_results = requests.get(url)

    ship_name = search_results.json()["name"]
    SHIP_ID_TO_NAME_DICT[ship_type_id] = ship_name
    return ship_name
