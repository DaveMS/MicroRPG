from actions.attack_action import AttackActionResponse
from actions.drop_action import DropActionResponse
from actions.equip_action import EquipActionResponse
from actions.move_action import MoveActionResponse
from actions.pickup_action import PickupActionResponse
from actions.unequip_action import UnequipActionResponse

action_response_text = {

    AttackActionResponse.no_weapon: "You have no weapon to attack with",
    DropActionResponse.item_not_in_inventory: "Item is not in your inventory",
    EquipActionResponse.item_not_in_inventory: "Item is not in your inventory",
    EquipActionResponse.item_is_not_equipable: "Item is not equipable",
    EquipActionResponse.item_is_already_equipped: "Item is already equipped",
    EquipActionResponse.no_slots_free_to_equip: "No slots free to equip this item",
    PickupActionResponse.item_not_in_room: "Item is not in this room",
    UnequipActionResponse.item_not_in_inventory: "Item is not in your inventory",
    UnequipActionResponse.item_is_not_equipped: "Item is not equipped"

}
