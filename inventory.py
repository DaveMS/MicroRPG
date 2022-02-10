class Inventory:

    def __init__(self, items=[]):
        self.contents = items

    def add_item(self, item):
        self.contents.append(item)

    def remove_item(self, item):
        self.contents.remove(item)

    def get_weight(self):
        weight = 0
        for item in self.contents:
            weight += item.weight
        return weight

    def get_equipped_weapons(self):
        weapons = []
        for item in self.contents:
            if item.equipable is not None and item.equipable.is_equipped() and item.weapon is not None:
                weapons.append(item)
        return weapons
