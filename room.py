from uuid import uuid4


class Room:

    def __init__(self, room_description, monsters=[], items=[]):
        self.id = uuid4()
        self.description = room_description
        self.monsters = monsters
        self.items = items
        self.exit_north_room_id = None
        self.exit_east_room_id = None
        self.exit_south_room_id = None
        self.exit_west_room_id = None

    def get_monsters(self):
        return [x for x in self.monsters if x.is_alive]
