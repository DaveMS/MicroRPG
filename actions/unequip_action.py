from enum import Enum

class UnequipAction:

  def __init__(self, character_id, item_id):
    self.character_id = character_id
    self.item_id = item_id

class UnequipActionResponse(Enum):
  ok = 1,
  item_not_in_inventory = 2,
  item_is_not_equipped = 3