class EndTurnActionHandler:

    def __init__(self, dungeon):
        self.dungeon = dungeon

    def perform_action(self, action):
        character = self.dungeon.get_character_by_id(action.character_id)
        return character.end_turn()
