from character import Character
from user_interface.utilities import get_user_input
from attributes import Attributes
from skills import Skills
from anatomy_creation_helpers import create_humanoid_anatomy
from item_creation_helpers import create_item


def create_character(dungeon):
    success, name = get_user_input("Enter a name for your character: ", convert_to_lower=False, allow_cancel=False)
    dagger = create_item("dagger")
    leather = create_item("leather_chest")
    helm = create_item("iron_helm")

    char = Character(
        name,
        5, 8,
        [
            dagger,
            leather,
            helm
        ],
        create_humanoid_anatomy(),
        Attributes(15, 10, 12),
        Skills(attack=15, defence=15),
        dungeon)

    char.equip_item(dagger.id, False)
    char.equip_item(leather.id, False)
    char.equip_item(helm.id, False)
    return char
