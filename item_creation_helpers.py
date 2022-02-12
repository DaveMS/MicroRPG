from item import Item
from weapon import Weapon
from equipable import Equipable
from armour import Armour
from usable import Usable
from body_part_type import BodyPartType
from dice_rolls import DiceRoll


def create_item(item_type):
    if item_type == "necklace":
        return __create_necklace()

    if item_type == "boots":
        return __create_boots()

    if item_type == "dagger":
        return __create_dagger()

    if item_type == "leather_chest":
        return __create_leather_chest()

    if item_type == "short_sword":
        return __create_short_sword()

    if item_type == "iron_helm":
        return __create_iron_helm()

    return None


def __create_necklace():
    return Item(
        name := "necklace",
        weight := 1,
        equipable := Equipable([BodyPartType.neck])
    )


def __create_boots():
    return Item(
        name="boots",
        weight=3,
        equipable=Equipable([BodyPartType.foot, BodyPartType.foot])
    )


def __create_dagger():
    return Item(
        name="dagger",
        weight=2,
        equipable=Equipable([BodyPartType.hand]),
        weapon=Weapon(DiceRoll(2, 4), DiceRoll(1, 6), 3)
    )


def __create_short_sword():
    return Item(
        name="short sword",
        weight=5,
        equipable=Equipable([BodyPartType.hand]),
        weapon=Weapon(DiceRoll(2, 8), DiceRoll(1, 8), 4)
    )


def __create_leather_chest():
    return Item(
        name="leather armour",
        weight=9,
        equipable=Equipable([BodyPartType.chest]),
        armour=Armour(protection=4, durability=40)
    )


def __create_iron_helm():
    return Item(
        name="iron helmet",
        weight=6,
        equipable=Equipable([BodyPartType.head]),
        armour=Armour(protection=6, durability=50)
    )
