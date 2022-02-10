from actions.move_action import MoveAction
from actions.attack_action import AttackAction
from actions.drop_action import DropAction
from actions.equip_action import EquipAction
from actions.pickup_action import PickupAction
from actions.unequip_action import UnequipAction
from action_handlers.move_action_handler import MoveActionHandler
from action_handlers.attack_action_handler import AttackActionHandler
from action_handlers.drop_action_handler import DropActionHandler
from action_handlers.equip_action_handler import EquipActionHandler
from action_handlers.pickup_action_handler import PickupActionHandler
from action_handlers.unequip_action_handler import UnequipActionHandler


class ActionHandler:

    def __init__(self, dungeon):
        self.__dungeon = dungeon
        self.__actionHandlers = {
            AttackAction.__name__: AttackActionHandler(dungeon),
            MoveAction.__name__: MoveActionHandler(dungeon),
            DropAction.__name__: DropActionHandler(dungeon),
            EquipAction.__name__: EquipActionHandler(dungeon),
            PickupAction.__name__: PickupActionHandler(dungeon),
            UnequipAction.__name__: UnequipActionHandler(dungeon)
        }

    def handle_action(self, action):
        return self.__actionHandlers[action.__class__.__name__].perform_action(action)
