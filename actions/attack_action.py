from enum import Enum


class AttackAction:

    def __init__(self, character_id, target_id, with_item_id=None):
        self.character_id = character_id
        self.target_id = target_id
        self.with_item_id = with_item_id


class AttackActionResponse(Enum):
    ok = 1,
    no_weapon = 2
