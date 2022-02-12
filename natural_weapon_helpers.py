from weapon import Weapon
from item import Item
from equipable import Equipable
from body_part_type import BodyPartType
from dice_rolls import DiceRoll


def create_kick():
    return Item(
        name="kick",
        weight=0,
        equipable=Equipable([BodyPartType.hand], False),
        weapon=Weapon(DiceRoll(1, 2), DiceRoll(1, 2), 2)
    )
