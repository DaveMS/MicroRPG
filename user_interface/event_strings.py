import events


class EventStrings:

    def __init__(self, dungeon):
        self.__dungeon = dungeon
        self.__event_handlers = {
            events.AttackHitEvent.__name__: self.__attack_hit_event,
            events.DiedEvent.__name__: self.__died_event,
            events.AttackMissedEvent.__name__: self.__attack_missed_event,
            events.AttackBlockedByArmourEvent.__name__: self.__attack_blocked_by_armour_event,
            events.TurnEndedEvent.__name__: self.__turn_ended_event
        }

    def event_to_string(self, event):
        return self.__event_handlers[event.__class__.__name__](event)

    def __attack_hit_event(self, event):
        attacker = self.__dungeon.get_character_by_id(event.attacker_id)
        target = self.__dungeon.get_character_by_id(event.target_id)
        target_body_part = target.anatomy.get_body_part_by_id(event.body_part_id)
        weapons = attacker.get_weapons()
        weapon = next((x for x in weapons if x.id == event.weapon_id), None)
        return f"{attacker.name} attacks {target.name}'s {target_body_part.name} with a {weapon.name} for {event.damage}  damage."

    def __attack_missed_event(self, event):
        attacker = self.__dungeon.get_character_by_id(event.attacker_id)
        target = self.__dungeon.get_character_by_id(event.target_id)
        weapons = attacker.get_weapons()
        weapon = next((x for x in weapons if x.id == event.weapon_id), None)
        return f"{attacker.name} attacks {target.name} with a {weapon.name}, but missed!"

    def __attack_blocked_by_armour_event(self, event):
        attacker = self.__dungeon.get_character_by_id(event.attacker_id)
        target = self.__dungeon.get_character_by_id(event.target_id)
        target_body_part = target.anatomy.get_body_part_by_id(event.body_part_id)
        weapons = attacker.get_weapons()
        weapon = next((x for x in weapons if x.id == event.weapon_id), None)
        return f"{attacker.name} attacks {target.name}'s {target_body_part.name} with a {weapon.name}, but it is blocked by {target_body_part.equipped_item.name}."

    def __died_event(self, event):
        character = self.__dungeon.get_character_by_id(event.character_id)
        return f"{character.name} died!"

    def __turn_ended_event(self, event):
        character = self.__dungeon.get_character_by_id(event.character_id)
        return f"{character.name} ended their turn."
