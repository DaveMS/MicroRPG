from user_interface.user_interface import UserInterface

from character_controller import CharacterController


class PlayerController(CharacterController):

    def get_action(self, error):
        return self.__user_interface.get_user_action(error)

    def __init__(self, user_interface):
        self.__user_interface = user_interface
