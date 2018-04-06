import eve

class Character(object):

    def __init__(self, character_id, character_name):
        self.id = character_id
        self.name = character_name
        self.kills = []
        self.losses = []

        #these currently only gett updated when you call get_info
        self.cyno_loss_count = 0
        self.carrier_loss_count = 0
        self.blops_kill_count = 0

    def update_kill_and_loss_counts(self):
        for kill in self.kills:
            if kill.blops:
                self.blops_kill_count += 1

        for loss in self.losses:
            if loss.carrier:
                self.carrier_loss_count += 1
            if loss.had_cyno():
                self.cyno_loss_count += 1

    def get_info(self):
        self.update_kill_and_loss_counts()
        json_info = {}
        json_info["id"] = self.id
        json_info["name"] = self.name

        json_info["cyno_loss_count"] = self.cyno_loss_count
        json_info["carrier_loss_count"] = self.carrier_loss_count
        json_info["blops_kill_count"] = self.blops_kill_count

        json_info["scary"] = False
        if self.cyno_loss_count > 0 or self.blops_kill_count > 0:
            json_info["scary"] = True

        important_losses_info = []
        for loss in self.losses:
            if loss.is_important_loss():
                important_losses_info.append(loss.get_info())

        json_info["important_losses"] = important_losses_info

        important_kills_info = []
        for kill in self.kills:
            if kill.is_important_kill():
                important_kills_info.append(kill.get_info())

        json_info["important_kills"] = important_kills_info
        return json_info
