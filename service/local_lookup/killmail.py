
from . import esi
from . import item

CARRIERS = [23919, 23917, 23915, 23913, 23911, 24483, 22852, 23757]
BLOPS = [22436, 22430, 22428, 22440, 44996]

class Killmail(object):

    def __init__(self, raw_mail):
        self.killmail_id = raw_mail.get("killmail_id")
        self.killmail_time = raw_mail.get("killmail_time")
        self.victim_id = raw_mail["victim"].get("character_id")
        self.ship_id = raw_mail["victim"].get("ship_type_id")
        self.npc_kill = False
        self.blops = False
        self.carrier = False
        self.attackers = []
        self.items = []

        if self.victim_id == None:
            self.npc_kill = True

        for attacker in raw_mail["attackers"]:
            attacker_id = attacker.get("character_id")
            if attacker_id != None:
                self.attackers.append(attacker_id)

        self.ship_name = esi.get_ship_name(self.ship_id)

        if self.ship_id in BLOPS:
            self.blops = True

        if self.ship_id in CARRIERS:
            self.carrier = True

        self.__process_items(raw_mail)


    def __process_items(self, raw_mail):
        raw_victim = raw_mail["victim"]
        for raw_item in raw_victim["items"]:
            item_obj = item.Item(raw_item["item_type_id"])
            self.items.append(item_obj)


    def is_important_loss(self):
        if self.had_cyno():
            return True
        if self.carrier:
            return True
        return False


    def is_important_kill(self):
        if self.blops:
            return True
        return False


    def had_cyno(self):
        for item_obj in self.items:
            if item_obj.is_cyno():
                return True
        return False


    #currently carrier and blops kills are not marked as scary
    #not sure how we want to handle things
    def get_info(self):
        json_info = {}
        json_info["killmail_id"] = self.killmail_id
        json_info["killmail_time"] = self.killmail_time
        json_info["ship_name"] = self.ship_name
        json_info["scary"] = False
        json_info["blops"] = self.blops
        json_info["carrier"] = self.carrier
        important_items_info = []
        for item_obj in self.items:
            if item_obj.is_important():
                json_info["scary"] = True
                important_items_info.append(item_obj.get_info())

        if self.blops:
            json_info["scary"] = True

        json_info["important_items"] = important_items_info

        return json_info