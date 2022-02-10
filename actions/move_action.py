from enum import Enum

class MoveAction:

  def __init__(self, character_id, room_id):
    self.character_id = character_id
    self.room_id = room_id

class MoveActionResponse(Enum):
  ok = 1