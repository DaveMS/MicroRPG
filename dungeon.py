from monster_creation_helpers import create_monster
from item_creation_helpers import create_item
from room import Room


class Dungeon:

    def __init__(self):
        self.rooms = []
        self.items = []
        self.characters = []
        self.current_room = None
        self.player = None
        self.event_handler = lambda evnt: None

    def add_player(self, player):
        self.player = player
        self.characters.append(player)

    def new_turn(self):
        for character in self.__get_all_characters():
            character.has_ended_turn = False
            character.add_action_points_for_new_turn()

    def perform_ai_turns(self):
        for monster in self.current_room.get_monsters():
            monster.attack(self.player)

    def get_next_character_to_act(self):
        if not self.player.has_ended_turn:
            return self.player

        for monster in self.current_room.get_monsters():
            if monster.is_alive and not monster.has_ended_turn:
                return monster

        return None

    def num_enemies_alive(self):
        enemies_alive = 0
        for room in self.rooms:
            enemies_alive += len(room.get_monsters())
        return enemies_alive

    def get_character_by_id(self, character_id):
        return next((x for x in self.__get_all_characters() if x.id == character_id), None)

    def get_characters_by_id(self, character_ids):
        return [x for x in self.__get_all_characters() if x.id in character_ids]

    def get_room_by_id(self, room_id):
        return next((x for x in self.rooms if x.id == room_id), None)

    def get_item_by_id(self, item_id):
        return next((x for x in self.items if x.id == item_id), None)

    def get_items_by_ids(self, item_ids):
        return [x for x in self.items if x.id in item_ids]

    def __get_all_characters(self):
        characters = [self.player]
        for room in self.rooms:
            characters.extend(room.get_monsters())
        return characters
