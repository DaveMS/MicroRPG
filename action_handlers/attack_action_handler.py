class AttackActionHandler:
  
  def __init__(self, dungeon):
    self.dungeon = dungeon

  def perform_action(self, action):
    attacker = self.dungeon.get_character_by_id(action.character_id)
    target = self.dungeon.get_character_by_id(action.target_id)
    return attacker.attack(target, action.with_item_id)
