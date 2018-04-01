from xml.etree import ElementTree
import requests

class EveApi(object):

    def __init__(self):
        pass

    #takes in a list of character names
    #returns a list of Characters
    def get_characters(self, character_names):
        characters = []
        character_name_csv = ",".join(character_names)
        url = "https://api.eveonline.com/eve/CharacterID.xml.aspx?names=" + character_name_csv
        print(url)
        search_results = requests.get(url)
        print("finished request")
        root = ElementTree.fromstring(search_results.content)
        rowset = root.find('.//rowset[@name="characters"]')
        for row in rowset.findall("row"):
            character_name = row.get('name')
            character_id = int(row.get('characterID'))
            character = Character(character_id, character_name)
            characters.append(character)
        return characters

    #takes in a list of Characters
    #returns a dictionary of character ids to loss mails
    def get_character_losses(self, characters):
        character_lossmail_map = {}
        character_ids = []
        for character in characters:
            character_lossmail_map[character.id] = []
            character_ids.append(character.id)

        #zkillboard requires the ids to be sorted for its api
        character_ids.sort()
        character_id_str = ",".join(str(i) for i in character_ids)
        url = "https://zkillboard.com/api/losses/characterID/" + character_id_str + "/"
        headers = {'Accept-Encoding': 'gzip', 'User-Agent': 'naabers'}
        search_results = requests.get(url, headers=headers)
        lossmails = search_results.json()

        for lossmail in lossmails:
            victim = lossmail["victim"]
            #should probably do some error checking here and not trust that zkillboard only returned
            #us results that we asked for
            character_lossmail_map[victim["character_id"]].append(lossmail)

        return character_lossmail_map

    def get_ship_name(self, ship_type_id):
        url = "https://esi.tech.ccp.is/latest/universe/types/" + ship_type_id + "/"
        search_results = requests.get(url)

        return search_results.json()["name"]

class Character(object):

    def __init__(self, id, name):
        self.api = EveApi()
        self.id = id
        self.name = name
        self.scary = False
        self.losses = []
        self.cyno_ships = []

    def set_losses(self, losses):
        self.losses = losses
        self.__process_losses()

    def is_scary(self):
        return self.scary

    def get_info(self):
        json_info = {}
        json_info["id"] = self.id
        json_info["name"] = self.name
        json_info["scary"] = self.scary
        json_info["cyno_ships"] = self.cyno_ships
        return json_info

    def __process_losses(self):
        for lossmail in self.losses:
            victim = lossmail["victim"]
            for item in victim["items"]:
                item_type_id = item["item_type_id"]
                if self.__is_scary_item(item_type_id):
                    self.scary = True
                    self.cyno_ships.append(self.api.get_ship_name(str(victim["ship_type_id"])))


    # Items:
    # cyno:        21096
    # covert cyno: 28646
    def __is_scary_item(self, item_type_id):
        if item_type_id == 21096:
            return True
        elif item_type_id == 28646:
            return True
        return False

    def __get_scary_item_name(self, item_type_id):
        if item_type_id == 21096:
            return "cyno"
        elif item_type_id == 28646:
            return "covert cyno"
        return ""

