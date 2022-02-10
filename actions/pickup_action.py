from enum import Enum

class PickupAction:

  def __init__(self, character_id, item_id):
    self.character_id = character_id
    self.item_id = item_id

class PickupActionResponse(Enum):
  ok = 1,
  item_not_in_room = 2