from item import Item


class Equipable():

    def __init__(self, equip_slots):
        self.equip_slots = equip_slots
        self.equipped_body_parts = []

    def is_equipped(self):
        return len(self.equipped_body_parts) > 0
