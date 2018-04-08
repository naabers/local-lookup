
# Items:
    # cyno:        21096
    # covert cyno: 28646
class Item(object):

    def __init__(self, item_id):
        self.id = item_id
        self.name = ""
        self.scary = False
        self.cyno = False

        if self.id == 21096:
            self.scary = True
            self.cyno = True
            self.name = "cyno"
        elif self.id == 28646:
            self.scary = True
            self.cyno = True
            self.name = "covert cyno"


    def is_cyno(self):
        if self.id == 21096 or self.id == 28646:
            return True
        return False


    def is_important(self):
        return self.scary


    def get_info(self):
        json_info = {}
        json_info["name"] = self.name
        json_info["scary"] = self.scary
        json_info["cyno"] = self.cyno
        return json_info