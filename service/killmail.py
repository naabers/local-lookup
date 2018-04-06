import item

import eve

class Killmail(object):

    def __init__(self, raw_mail):
        self.victim_id = raw_mail["victim"]["character_id"]
        self.ship_id = raw_mail["victim"]["ship_type_id"]

        self.ship_name = eve.get_ship_name(self.ship_id)

        self.items = []
        self.__process_items(raw_mail)

    def __process_items(self, raw_mail):
        raw_victim = raw_mail["victim"]
        for raw_item in raw_victim["items"]:
            item_obj = item.Item(raw_item["item_type_id"])
            self.items.append(item_obj)

    #can later add to this for ship types, etc
    def is_important(self):
        for item_obj in self.items:
            if item_obj.scary:
                return True
        return False

    def get_info(self):
        json_info = {}

        json_info["ship_name"] = self.ship_name
        json_info["scary"] = False

        important_items_info = []
        for item_obj in self.items:
            if item_obj.is_important():
                json_info["scary"] = True
                important_items_info.append(item_obj.get_info())

        json_info["important_items"] = important_items_info

        return json_info
