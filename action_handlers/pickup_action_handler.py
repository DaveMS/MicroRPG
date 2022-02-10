class PickupActionHandler:
  
  def __init__(self, dungeon):
    self.dungeon = dungeon

  def perform_action(self, action):
    character = self.dungeon.get_character_by_id(action.character_id)
    return character.pickup_item(action.item_id)

