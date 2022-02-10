import random
from inventory import Inventory
from uuid import uuid4
from actions.attack_action import AttackActionResponse
from actions.equip_action import EquipActionResponse
from actions.unequip_action import UnequipActionResponse
from actions.pickup_action import PickupActionResponse
from actions.drop_action import DropActionResponse
from actions.move_action import MoveActionResponse
import events
from dice_rolls import DiceRoll
import math


class Character:

    def __init__(self, name, items, anatomy, attributes, skills, dungeon):
        self.id = uuid4()
        self.name = name
        self.is_alive = True
        self.inventory = Inventory(items)
        self.anatomy = anatomy
        self.attributes = attributes
        self.skills = skills
        self.room_id = None
        self.__dungeon = dungeon

    def take_damage(self, damage, body_part):
        body_part.take_damage(damage)
        if self.anatomy.has_fatal_damage():
            self.__die()

    def get_weapons(self):
        available_natural_weapons = self.anatomy.get_natural_weapons()
        equipped_weapons = self.inventory.get_equipped_weapons()
        weapons = available_natural_weapons + equipped_weapons
        return weapons

    def attack(self, target):
        weapons = self.get_weapons()
        if len(weapons) == 0:
            return False, AttackActionResponse.no_weapon

        weapon = random.choice(weapons)

        attack = self.skills.attack + DiceRoll(1, 6).roll()
        defence = target.skills.defence + DiceRoll(1, 6).roll()

        if defence >= attack:
            self.__dungeon.event_handler(events.AttackMissedEvent(self.id, target.id, weapon.id))
            return True, AttackActionResponse.ok

        body_part = target.anatomy.get_random_body_part_on_hit_distribution()

        armour = None
        if body_part.equipped_item is not None:
            armour = body_part.equipped_item.armour

        has_penetrated_armour = True
        if armour is not None:
            armour_pen_roll = weapon.weapon.armour_pen_roll.roll()
            modified_protection = armour.adjusted_protection()
            has_penetrated_armour = armour_pen_roll > modified_protection

        damage = weapon.weapon.damage_roll.roll()

        if has_penetrated_armour:
            self.__dungeon.event_handler(events.AttackHitEvent(self.id, target.id, weapon.id, body_part.id, damage))
            target.take_damage(damage, body_part)
        else:
            self.__dungeon.event_handler(events.AttackBlockedByArmourEvent(self.id, target.id, weapon.id, body_part.id,
                                                                           body_part.equipped_item.id, damage))
            armour.durability = max(armour.durability - damage, 0)

        return True, AttackActionResponse.ok

    def __die(self):
        self.is_alive = False
        self.__dungeon.current_room.items.extend(self.inventory.contents)
        self.items = []
        self.__dungeon.event_handler(events.DiedEvent(self.id))

    def move(self, to_room_id):
        self.__dungeon.current_room = self.__dungeon.get_room_by_id(to_room_id)
        self.room_id = to_room_id
        return True, MoveActionResponse.ok

    def equip_item(self, item_id):
        item = next((x for x in self.inventory.contents if x.id == item_id), None)
        if item is None:
            return False, EquipActionResponse.item_not_in_inventory

        if item.equipable is None:
            return False, EquipActionResponse.item_is_not_equipable

        if item.equipable.is_equipped():
            return False, EquipActionResponse.item_is_already_equipped

        if not self.anatomy.has_equip_slots_free(item.equipable.equip_slots):
            return False, EquipActionResponse.no_slots_free_to_equip

        self.anatomy.equip_item(item)
        return True, EquipActionResponse.ok

    def unequip_item(self, item_id):
        item = next((x for x in self.inventory.contents if x.id == item_id), None)

        if item is None:
            return False, UnequipActionResponse.item_not_in_inventory

        if item.equipable is None or not item.equipable.is_equipped():
            return False, UnequipActionResponse.item_is_not_equipped

        self.anatomy.unequip_item(item)
        return True, UnequipActionResponse.ok

    def pickup_item(self, item_id):
        room = self.__dungeon.get_room_by_id(self.room_id)
        item_to_pickup = next((x for x in room.items if x.id == item_id), None)
        if item_to_pickup is None:
            return False, PickupActionResponse.item_not_in_room

        self.inventory.add_item(item_to_pickup)
        room.items.remove(item_to_pickup)
        return True, PickupActionResponse.ok

    def drop_item(self, item_id):
        item = next((x for x in self.inventory.contents if x.id == item_id), None)
        if item is None:
            return False, DropActionResponse.item_not_in_inventory

        if item.equipable.is_equipped():
            self.unequip_item(item_id)

        current_room = self.__dungeon.get_room_by_id(self.room_id)
        self.inventory.remove_item(item)
        current_room.items.append(item)
        return True, DropActionResponse.ok
