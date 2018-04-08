from . import character
from . import eve_xml
from . import zkill


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


def get_character_information(character_names):
    character_names = character_names.split(",")
    character_id_map = eve_xml.get_character_ids(character_names)

    characters = []
    for character_id, character_name in character_id_map.items():
        character_obj = character.Character(character_id, character_name)
        characters.append(character_obj)

    killmails = zkill.get_character_killmails(character_id_map)
    process_killmails(characters, killmails)

    processed_data = []
    for character_obj in characters:
        processed_data.append(character_obj.get_info())

    return processed_data