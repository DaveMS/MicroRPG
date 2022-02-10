from uuid import uuid4


class Item:

    def __init__(self, name, weight, equipable=None, weapon=None, armour=None):
        self.id = uuid4()
        self.name = name
        self.weight = weight
        self.equipable = equipable
        self.weapon = weapon
        self.armour = armour
