from enum import Enum


class EndTurnAction:

    def __init__(self, character_id):
        self.character_id = character_id


class EndTurnActionResponse(Enum):
    ok = 1
