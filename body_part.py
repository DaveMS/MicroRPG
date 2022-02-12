from uuid import uuid4


class BodyPart:

    def __init__(self, name, body_part_type, health, chance_to_hit, loss_is_fatal=False, natural_weapon=None,
                 child_body_parts=[]):
        self.id = uuid4()
        self.name = name
        self.body_part_type = body_part_type
        self.health = health
        self.max_health = health
        self.child_body_parts = child_body_parts
        self.chance_to_hit = chance_to_hit
        self.equipped_item = None
        self.loss_is_fatal = loss_is_fatal
        self.natural_weapon = natural_weapon
        
        if self.natural_weapon is not None:
          self.natural_weapon.equipable.equipped_body_parts = [ self ]

    def print_body_part_status(self, nesting_level=0):
        base_status = "   " * nesting_level + f" {self.name} {self.health}/{self.max_health}"

        if self.equipped_item is not None:
            base_status += f"  equipped: {self.equipped_item.name}"

        print(base_status)
        for child_body_part in self.child_body_parts:
            child_body_part.print_body_part_status(nesting_level + 1)

    def get_all_descendants_parts(self):
        parts = [self]
        for body_part in self.child_body_parts:
            parts.extend(body_part.get_all_descendants_parts())
        return parts

    def take_damage(self, damage_amount):
        self.health -= damage_amount
        if self.health < 0:
            self.health = 0
