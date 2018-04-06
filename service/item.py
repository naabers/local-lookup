
# Items:
    # cyno:        21096
    # covert cyno: 28646
class Item(object):

    def __init__(self, item_id):
        self.id = item_id
        self.name = ""
        self.scary = False
        if self.id == 21096:
            self.scary = True
            self.name = "cyno"
        elif self.id == 28646:
            self.scary = True
            self.name = "covert cyno"

    def is_important(self):
        return self.scary

    def get_info(self):
        json_info = {}
        json_info["name"] = self.name
        json_info["scary"] = self.scary
        return json_info
