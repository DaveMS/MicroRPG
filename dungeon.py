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

    def perform_ai_turns(self):
        for monster in self.current_room.monsters:
            if monster.is_alive:
                monster.attack(self.player)

    def num_enemies_alive(self):
        enemies_alive = 0
        for room in self.rooms:
            for monster in room.monsters:
                if monster.is_alive:
                    enemies_alive += 1
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
            characters.extend(room.monsters)
        return characters
