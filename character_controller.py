from abc import ABC, abstractmethod


class CharacterController(ABC):

    @abstractmethod
    def get_action(self, error):
        pass
