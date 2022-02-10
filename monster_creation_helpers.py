from character import Character
from attributes import Attributes
from skills import Skills
from item_creation_helpers import create_item
from anatomy_creation_helpers import create_humanoid_anatomy


def create_monster(monster_type, dungeon):
    if monster_type == "goblin":
        return __create_goblin(dungeon)

    if monster_type == "skeleton":
        return __create_skeleton(dungeon)


def __create_goblin(dungeon):
    dagger = create_item("dagger")
    char = Character("Goblin", [
        create_item("boots"),
        dagger
    ], create_humanoid_anatomy(0.5), Attributes(6, 12, 4), Skills(attack=12, defence=14), dungeon)
    char.equip_item(dagger.id)
    return char


def __create_skeleton(dungeon):
    leather = create_item("leather_chest")
    sword = create_item("short_sword")
    char = Character("Skeleton", [
        create_item("necklace"),
        leather,
        sword
    ], create_humanoid_anatomy(0.75), Attributes(8, 5, 2), Skills(attack=15, defence=13), dungeon)
    char.equip_item(leather.id)
    char.equip_item(sword.id)
    return char
