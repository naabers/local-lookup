import requests
from xml.etree import ElementTree

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
