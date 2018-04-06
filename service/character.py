import eve

class Character(object):

    def __init__(self, character_id, character_name):
        self.id = character_id
        self.name = character_name
        self.losses = []
        self.cyno_ships = []

    def get_info(self):
        json_info = {}
        json_info["id"] = self.id
        json_info["name"] = self.name
        json_info["scary"] = False

        important_losses_info = []
        for loss in self.losses:
            if loss.is_important():
                json_info["scary"] = True
                important_losses_info.append(loss.get_info())

        json_info["important_losses"] = important_losses_info
        return json_info
