import random
from weapon import Weapon


class Anatomy:

    def __init__(self, body_parts):
        self.body_parts = body_parts

    def print_anatomy_status(self):
        for body_part in self.body_parts:
            body_part.print_body_part_status()

    def get_body_part_by_id(self, id):
        for body_part in self.__flatten_body_part_tree():
            if body_part.id == id:
                return body_part
        return None

    def has_fatal_damage(self):
        body_part_list = self.__flatten_body_part_tree()
        fatal_body_parts = [x for x in body_part_list if x.loss_is_fatal and x.health == 0]
        total_health = sum(map(lambda x: x.health, body_part_list))
        return len(fatal_body_parts) > 0 or total_health == 0

    def has_equip_slots_free(self, equip_slots):
        body_part_list = self.__flatten_body_part_tree()
        for equip_slot in equip_slots:
            available_body_part = self.__get_body_part_with_free_equip_slot(equip_slot, body_part_list)
            if available_body_part is None:
                return False
            body_part_list.remove(available_body_part)
        return True

    def get_random_body_part_on_hit_distribution(self):
        body_parts_list = self.__flatten_body_part_tree()
        return next(iter(random.choices(body_parts_list, weights=map(lambda x: x.chance_to_hit, body_parts_list), k=1)),
                    None)

    def get_natural_weapons(self):
        body_parts = self.__flatten_body_part_tree()
        return list(map(lambda y: y.natural_weapon, [x for x in body_parts if x.natural_weapon is not None]))

    def equip_item(self, item):
        if not self.has_equip_slots_free(item.equipable.equip_slots):
            return
        body_part_list = self.__flatten_body_part_tree()
        equipped_body_parts = []
        for equip_slot in item.equipable.equip_slots:
            available_body_part = self.__get_body_part_with_free_equip_slot(equip_slot, body_part_list)
            available_body_part.equipped_item = item
            equipped_body_parts.append(available_body_part)
        item.equipable.equipped_body_parts = equipped_body_parts

    def unequip_item(self, item):
        equipped_body_parts = item.equipable.equipped_body_parts
        for body_part in equipped_body_parts:
            body_part.equipped_item = None
        item.equipable.equipped_body_parts = []

    def __flatten_body_part_tree(self):
        body_part_list = []
        for part in self.body_parts:
            body_part_list.extend(part.get_all_descendants_parts())
        return body_part_list

    def __get_body_part_with_free_equip_slot(self, equip_slot, from_body_parts=None):
        body_part_list = from_body_parts
        if body_part_list is None:
            body_part_list = self.__flatten_body_part_tree()
        return next((x for x in body_part_list if x.body_part_type == equip_slot and x.equipped_item == None), None)
