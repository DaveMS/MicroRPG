from enum import Enum

class EquipAction:

  def __init__(self, character_id, item_id):
    self.character_id = character_id
    self.item_id = item_id

class EquipActionResponse(Enum):
  ok = 1,
  item_not_in_inventory = 2,
  item_is_not_equipable = 3,
  item_is_already_equipped = 4,
  no_slots_free_to_equip = 5
  
  
  