class Game:

    def __init__(self, dungeon, player_character, user_interface, action_handler):
        self.__dungeon = dungeon
        self.__user_interface = user_interface
        self.__action_handler = action_handler
        self.__player_character = player_character

    def start(self):
        self.__dungeon.event_handler = self.__handle_event

        is_game_over = False
        while not is_game_over:
            self.__take_player_turn()
            self.__dungeon.perform_ai_turns()
            input("Press enter to continue")
            is_game_over = self.__dungeon.num_enemies_alive() == 0 or not self.__player_character.is_alive

    def __take_player_turn(self):
        has_player_taken_turn = False
        error = None
        while not has_player_taken_turn:
            has_player_taken_turn, action = self.__user_interface.get_user_action(error)
            has_player_taken_turn, error = self.__action_handler.handle_action(action)

    def __handle_event(self, event):
        self.__user_interface.handle_event(event)
