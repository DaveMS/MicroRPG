import math


class Armour:

    def __init__(self, protection, durability):
        self.protection = protection
        self.durability = durability
        self.max_durability = durability

    def adjusted_protection(self):
        return int(math.ceil(self.protection * (self.durability / self.max_durability)))
