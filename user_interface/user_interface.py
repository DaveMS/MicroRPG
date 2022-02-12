from actions.end_turn_action import EndTurnAction
from actions.move_action import MoveAction
from actions.pickup_action import PickupAction
from actions.equip_action import EquipAction
from actions.unequip_action import UnequipAction
from actions.drop_action import DropAction
from actions.attack_action import AttackAction
from events import TurnEndedEvent
from user_interface.action_response_text_mapping import action_response_text
from user_interface.event_strings import EventStrings

from user_interface.utilities import get_user_input, select_item, select_character_target, clear
import os


class UserInterface:

    def __init__(self, player, dungeon):
        self.__player = player
        self.__dungeon = dungeon
        self.__event_strings = EventStrings(self.__dungeon)

    def get_user_action(self, last_error=None):
        has_chosen_action = False
        action = None
        while not has_chosen_action:
            self.__display_game_state()
            has_chosen_action, action = self.__get_user_action(last_error)
        return True, action

    def handle_event(self, evnt):
        print(self.__event_strings.event_to_string(evnt))
        input("Press Enter to continue...")

    def __display_game_state(self):
        clear()
        print(self.__get_room_description(self.__dungeon.current_room))
        print()
        print(
            f"Player: {self.__player.name} AP: {self.__player.action_points}/{self.__player.max_action_points} (+{self.__player.action_points_per_turn} per turn)")
        print()

    def __get_room_description(self, room):
        desc = room.description + f"{os.linesep}{os.linesep}"
        alive_monsters = room.get_monsters()
        if len(alive_monsters) > 0:
            desc += f"{os.linesep}{os.linesep}You see some monsters:"
            for monster in alive_monsters:
                if monster.is_alive:
                    desc += f"{os.linesep} {monster.name}"
            desc += f"{os.linesep}{os.linesep}"

        if len(room.items) > 0:
            desc += f"{os.linesep}{os.linesep}There are some items on the floor:"
            for item in room.items:
                desc += f"{os.linesep} {item.name}"
            desc += f"{os.linesep}{os.linesep}"

        if room.exit_north_room_id is not None:
            desc += f"{os.linesep} There is an exit to the north"
        if room.exit_east_room_id is not None:
            desc += f"{os.linesep} There is an exit to the east"
        if room.exit_south_room_id is not None:
            desc += f"{os.linesep} There is an exit to the south"
        if room.exit_west_room_id is not None:
            desc += f"{os.linesep} There is an exit to the west"

        return desc

    def __get_user_action(self, last_error):
        root_actions = ["(m)ove", "(a)ttack", "(p)ickup", "(i)nventory", "(h)ealth", "(e)nd turn"]

        if last_error is not None:
            print(action_response_text[last_error])

        success, chosen_action = get_user_input("What would you like to do? ", root_actions, allow_cancel=False)

        if chosen_action in ("move", "m"):
            return self.__get_move_action()

        if chosen_action in ("attack", "a"):
            return self.__get_attack_action()

        if chosen_action in ("pickup", "p"):
            return self.__get_pickup_action()

        if chosen_action in ("inventory", "i"):
            return self.perform_inventory_action()

        if chosen_action in ("health", "h"):
            self.__view_health_screen()
            return False, None

        if chosen_action in ("end turn", "e"):
            return self.__get_end_turn_action()

    def __view_health_screen(self):
        clear()
        print("Health Status: ")
        self.__player.anatomy.print_anatomy_status()
        print()
        input("Press enter to continue...")

    def __get_end_turn_action(self):
        return True, EndTurnAction(self.__player.id)

    def __get_pickup_action(self):
        current_room = self.__dungeon.current_room
        has_selected, item_index = select_item("Select an item to pick up: ", current_room.items)
        if not has_selected:
            return False, None
        return True, PickupAction(self.__player.id, current_room.items[item_index].id)

    def perform_inventory_action(self):
        clear()
        print("Inventory: ")
        for item in self.__player.inventory.contents:
            print(f"{item.name} weight: {item.weight}", end="")
            if item.equipable is not None and item.equipable.is_equipped():
                print(f"  equipped on: ", end="")
                for body_part in item.equipable.equipped_body_parts:
                    print(f"{body_part.name}  ", end="")
            print()
        print()
        allowed_actions = ["e(x)amine", "(e)quip", "(u)se", "u(n)equip", "(d)rop", "(b)ack"]
        success, action_string = get_user_input("Select action: ", allowed_actions)

        if success:
            if action_string in ("examine", "x"):
                self.__examine_item_screen()
                return False, None

            if action_string in ("equip", "e"):
                return self.__get_equip_item_action()

            if action_string in ("drop", "d"):
                return self.__get_drop_item_action()

            if action_string in ("unequip", "n"):
                return self.perform_unequip_item_action()

            if action_string in ("use", "u"):
                return self.perform_use_item_action()

        return False, None

    def __examine_item_screen(self):
        return False, ""

    def __get_equip_item_action(self):
        equipable_items = [x for x in self.__player.inventory.contents if
                           x.equipable is not None and not x.equipable.is_equipped()]
        has_selected, item_index = select_item("select an item to equip: ", equipable_items)
        if not has_selected:
            return False, None
        return True, EquipAction(self.__player.id, equipable_items[item_index].id)

    def __get_drop_item_action(self):
        items = self.__player.inventory.contents
        has_selected, item_index = select_item("Select an item to drop: ", items)
        if not has_selected:
            return False, None
        return True, DropAction(self.__player.id, items[int(item_index)].id)

    def perform_unequip_item_action(self):
        equipped_items = [x for x in self.__player.inventory.contents if
                          x.equipable is not None and x.equipable.is_equipped()]
        has_selected, item_index = select_item("select an item to unequip: ", equipped_items)
        if not has_selected:
            return False, None
        return True, UnequipAction(self.__player.id, equipped_items[item_index].id)

    def perform_use_item_action(self, player):
        pass

    def __get_move_action(self):

        current_room = self.__dungeon.current_room

        valid_directions = []
        if current_room.exit_north_room_id is not None:
            valid_directions.append("(n)orth")
        if current_room.exit_east_room_id is not None:
            valid_directions.append("(e)ast")
        if current_room.exit_south_room_id is not None:
            valid_directions.append("(s)outh")
        if current_room.exit_west_room_id is not None:
            valid_directions.append("(w)est")

        success, direction = get_user_input("Which direction would you like to go? ", valid_directions)

        if not success:
            return False, None

        move_to_room_id = None
        if direction in ("north", "n"):
            move_to_room_id = current_room.exit_north_room_id
        if direction in ("east", "e"):
            move_to_room_id = current_room.exit_east_room_id
        if direction in ("south", "s"):
            move_to_room_id = current_room.exit_south_room_id
        if direction in ("west", "w"):
            move_to_room_id = current_room.exit_west_room_id

        return True, MoveAction(self.__player.id, move_to_room_id)

    def __get_attack_action(self):
        current_room = self.__dungeon.current_room

        possible_weapons = self.__player.get_weapons()
        for i in range(len(possible_weapons)):
          print(f"{i}) {possible_weapons[i].name} AP: {possible_weapons[i].weapon.action_point_cost}  ( ", end="")
          for body_part in possible_weapons[i].equipable.equipped_body_parts:
            print(f"{body_part.name}  ", end="")
          print(")")
        print()

        prompt = "Select a weapon to attack with: "
        allowed_values = [str(i) for i in range(len(possible_weapons))]
        success, index_string = get_user_input(prompt=prompt, print_allowed_values=False, allowed_values=allowed_values)

        if not success:
          return False, None

        selected_weapon = possible_weapons[int(index_string)]
        possible_targets = current_room.get_monsters()
        success, target_monster_index = select_character_target(possible_targets)
        if not success:
            return False, None
        return True, AttackAction(self.__player.id, possible_targets[target_monster_index].id, selected_weapon.id)
