from actions.end_turn_action import EndTurnAction
from player_controller import PlayerController


class Game:

    def __init__(self, dungeon, player_character, user_interface, action_handler):
        self.__dungeon = dungeon
        self.__user_interface = user_interface
        self.__action_handler = action_handler
        self.__player_character = player_character

    def start(self):
        self.__dungeon.event_handler = self.__handle_event
        self.__player_character.character_controller = PlayerController(self.__user_interface)

        is_game_over = False
        while not is_game_over:
            self.__dungeon.new_turn()
            self.__perform_turns()
            is_game_over = self.__dungeon.num_enemies_alive() == 0 or not self.__player_character.is_alive

    def __perform_turns(self):

        turns_complete = False
        while not turns_complete:
            next_character = self.__dungeon.get_next_character_to_act()
            if next_character is None:
                turns_complete = True
            else:
                self.__take_turn(next_character)

    def __take_turn(self, character):
        has_taken_turn = False
        action_is_successful = True
        error = None
        while not has_taken_turn:
            action_is_successful, action = character.character_controller.get_action(
                error if not action_is_successful else None)
            action_is_successful, error = self.__action_handler.handle_action(action)
            has_taken_turn = isinstance(action, EndTurnAction)

    def __take_player_turn(self):
        has_player_taken_turn = False
        action_is_successful = True
        error = None
        while not has_player_taken_turn:
            action_is_successful, action = self.__user_interface.get_user_action(
                error if not action_is_successful else None)
            action_is_successful, error = self.__action_handler.handle_action(action)
            has_player_taken_turn = isinstance(action, EndTurnAction)

    def __handle_event(self, event):
        self.__user_interface.handle_event(event)
