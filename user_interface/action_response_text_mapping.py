from actions.attack_action import AttackActionResponse
from actions.drop_action import DropActionResponse
from actions.equip_action import EquipActionResponse
from actions.move_action import MoveActionResponse
from actions.pickup_action import PickupActionResponse
from actions.unequip_action import UnequipActionResponse

action_response_text = {

    MoveActionResponse.not_enough_ap: "You do not have enough action points to move",
    AttackActionResponse.no_weapon: "You have no weapon to attack with",
    AttackActionResponse.not_enough_ap: "You do not have enough action points",
    DropActionResponse.item_not_in_inventory: "Item is not in your inventory",
    DropActionResponse.not_enough_ap: "You do not have enough action points to drop this item",
    EquipActionResponse.item_not_in_inventory: "Item is not in your inventory",
    EquipActionResponse.item_is_not_equipable: "Item is not equipable",
    EquipActionResponse.item_is_already_equipped: "Item is already equipped",
    EquipActionResponse.no_slots_free_to_equip: "No slots free to equip this item",
    EquipActionResponse.not_enough_ap: "You do not have enough action points to equip this item",
    PickupActionResponse.item_not_in_room: "Item is not in this room",
    PickupActionResponse.not_enough_ap: "You do not have enough action points to pickup this item",
    UnequipActionResponse.item_not_in_inventory: "Item is not in your inventory",
    UnequipActionResponse.item_is_not_equipped: "Item is not equipped",
    UnequipActionResponse.not_enough_ap: "You do not have enough action points to unequip this item"

}
