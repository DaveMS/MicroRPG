from dungeon import Dungeon
from room import Room
from monster_creation_helpers import create_monster
from item_creation_helpers import create_item


def create_dungeon():
    dungeon = Dungeon()

    room1 = Room("A starting room", [], [])

    room2 = Room("A room with monsters", [
        create_monster("goblin", dungeon)
    ], [])

    room3 = Room("Another room with more monsters", [
        create_monster("goblin", dungeon),
        create_monster("skeleton", dungeon)
    ], [
                     create_item("necklace")
                 ])

    room1.exit_east_room_id = room2.id
    room2.exit_west_room_id = room1.id
    room2.exit_north_room_id = room3.id
    room3.exit_south_room_id = room2.id

    dungeon.rooms = [room1, room2, room3]
    dungeon.current_room = room1
    return dungeon
