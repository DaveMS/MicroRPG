from weapon import Weapon
from item import Item
from dice_rolls import DiceRoll


def create_kick():
    return Item(
        name="kick",
        weight=0,
        equipable=None,
        weapon=Weapon(DiceRoll(1, 2), DiceRoll(1, 2))
    )
