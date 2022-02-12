import random

from actions.end_turn_action import EndTurnActionResponse
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

    def __init__(self, name, action_points, max_action_points, items, anatomy, attributes, skills, dungeon):
        self.id = uuid4()
        self.name = name
        self.is_alive = True
        self.inventory = Inventory(items)
        self.anatomy = anatomy
        self.attributes = attributes
        self.skills = skills
        self.room_id = None
        self.action_points = 0
        self.action_points_per_turn = action_points
        self.max_action_points = max_action_points
        self.has_ended_turn = False
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

    def attack(self, target, with_item_id=None):

        weapons = self.get_weapons()
        if len(weapons) == 0:
            return False, AttackActionResponse.no_weapon

        weapon_to_use = None
        if with_item_id is None:
            weapon_to_use = random.choice(weapons)
        else:
            for weapon in weapons:
                if weapon.id == with_item_id:
                    weapon_to_use = weapon

        if weapon_to_use is None:
            return False, AttackActionResponse.no_weapon

        if self.action_points < weapon_to_use.weapon.action_point_cost:
            return False, AttackActionResponse.not_enough_ap

        self.action_points -= weapon_to_use.weapon.action_point_cost
        attack = self.skills.attack + DiceRoll(1, 6).roll()
        defence = target.skills.defence + DiceRoll(1, 6).roll()

        if defence >= attack:
            self.__dungeon.event_handler(events.AttackMissedEvent(self.id, target.id, weapon_to_use.id))
            return True, AttackActionResponse.ok

        body_part = target.anatomy.get_random_body_part_on_hit_distribution()

        armour = None
        if body_part.equipped_item is not None:
            armour = body_part.equipped_item.armour

        has_penetrated_armour = True
        if armour is not None:
            armour_pen_roll = weapon_to_use.weapon.armour_pen_roll.roll()
            modified_protection = armour.adjusted_protection()
            has_penetrated_armour = armour_pen_roll > modified_protection

        damage = weapon_to_use.weapon.damage_roll.roll()

        if has_penetrated_armour:
            self.__dungeon.event_handler(
                events.AttackHitEvent(self.id, target.id, weapon_to_use.id, body_part.id, damage))
            target.take_damage(damage, body_part)
        else:
            self.__dungeon.event_handler(
                events.AttackBlockedByArmourEvent(self.id, target.id, weapon_to_use.id, body_part.id,
                                                  body_part.equipped_item.id, damage))
            armour.durability = max(armour.durability - damage, 0)

        return True, AttackActionResponse.ok

    def __die(self):
        self.is_alive = False
        self.__dungeon.current_room.items.extend(self.inventory.contents)
        self.items = []
        self.__dungeon.event_handler(events.DiedEvent(self.id))

    def move(self, to_room_id):
        if self.action_points < self.action_points_per_turn:
            return False, MoveActionResponse.not_enough_ap

        self.__dungeon.current_room = self.__dungeon.get_room_by_id(to_room_id)
        self.room_id = to_room_id
        self.action_points = 0
        return True, MoveActionResponse.ok

    def equip_item(self, item_id, use_action_points=True):
        item = next((x for x in self.inventory.contents if x.id == item_id), None)
        if item is None:
            return False, EquipActionResponse.item_not_in_inventory

        if item.equipable is None:
            return False, EquipActionResponse.item_is_not_equipable

        if item.equipable.is_equipped():
            return False, EquipActionResponse.item_is_already_equipped

        if not self.anatomy.has_equip_slots_free(item.equipable.equip_slots):
            return False, EquipActionResponse.no_slots_free_to_equip

        ap_required = min(self.max_action_points, item.weight)
        if use_action_points and self.action_points < ap_required:
            return False, EquipActionResponse.not_enough_ap

        self.anatomy.equip_item(item)
        if use_action_points:
            self.action_points -= ap_required
        return True, EquipActionResponse.ok

    def unequip_item(self, item_id):
        item = next((x for x in self.inventory.contents if x.id == item_id), None)

        if item is None:
            return False, UnequipActionResponse.item_not_in_inventory

        if item.equipable is None or not item.equipable.is_equipped():
            return False, UnequipActionResponse.item_is_not_equipped

        ap_required = min(self.max_action_points, item.weight)
        if self.action_points < ap_required:
            return False, UnequipActionResponse.not_enough_ap

        self.anatomy.unequip_item(item)
        return True, UnequipActionResponse.ok

    def pickup_item(self, item_id):
        room = self.__dungeon.get_room_by_id(self.room_id)
        item_to_pickup = next((x for x in room.items if x.id == item_id), None)
        if item_to_pickup is None:
            return False, PickupActionResponse.item_not_in_room

        ap_required = min(self.max_action_points, item_to_pickup.weight)
        if self.action_points < ap_required:
            return False, PickupActionResponse.not_enough_ap

        self.inventory.add_item(item_to_pickup)
        room.items.remove(item_to_pickup)
        return True, PickupActionResponse.ok

    def drop_item(self, item_id):
        item = next((x for x in self.inventory.contents if x.id == item_id), None)
        if item is None:
            return False, DropActionResponse.item_not_in_inventory

        ap_required = min(self.max_action_points, item.weight)
        if self.action_points < ap_required:
            return False, DropActionResponse.not_enough_ap

        if item.equipable.is_equipped():
            self.unequip_item(item_id)

        current_room = self.__dungeon.get_room_by_id(self.room_id)
        self.inventory.remove_item(item)
        current_room.items.append(item)
        return True, DropActionResponse.ok

    def end_turn(self):
        self.has_ended_turn = True
        self.__dungeon.event_handler(events.TurnEndedEvent(self.id))
        return True, EndTurnActionResponse.ok

    def add_action_points_for_new_turn(self):
        self.action_points = min(self.action_points + self.action_points_per_turn, self.max_action_points)
