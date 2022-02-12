from actions.attack_action import AttackAction
from actions.end_turn_action import EndTurnAction
from character_controller import CharacterController


class AIController(CharacterController):

    def get_action(self, error):
        if error:
            return True, EndTurnAction(self.__character.id)

        available_weapons = self.__character.get_weapons()
        weapon_to_use = None
        for weapon in sorted(available_weapons, key=lambda x: x.weapon.action_point_cost):
            if weapon.weapon.action_point_cost <= self.__character.action_points:
                weapon_to_use = weapon

        if weapon_to_use is None:
            return True, EndTurnAction(self.__character.id)

        return True, AttackAction(self.__character.id, self.__dungeon.player.id, weapon_to_use.id)

    def __init__(self, character, dungeon):
        self.__character = character
        self.__dungeon = dungeon
