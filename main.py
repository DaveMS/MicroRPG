from dungeon_generation import create_dungeon
from character_creation_helpers import create_character
from action_handler import ActionHandler
from game import Game
from user_interface.user_interface import UserInterface


def main():
    dungeon = create_dungeon()
    player_character = create_character(dungeon)
    dungeon.add_player(player_character)
    action_handler = ActionHandler(dungeon)
    user_interface = UserInterface(player_character, dungeon)

    game = Game(dungeon, player_character, user_interface, action_handler)

    game.start()


main()
