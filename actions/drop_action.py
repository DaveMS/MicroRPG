from enum import Enum

class DropAction:

  def __init__(self, character_id, item_id):
    self.character_id = character_id
    self.item_id = item_id

class DropActionResponse(Enum):
  ok = 1,
  item_not_in_inventory = 2