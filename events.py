class AttackHitEvent:
    def __init__(self, attacker_id, target_id, weapon_id, body_part_id, damage):
        self.attacker_id = attacker_id
        self.target_id = target_id
        self.weapon_id = weapon_id
        self.body_part_id = body_part_id
        self.damage = damage


class AttackBlockedByArmourEvent:
    def __init__(self, attacker_id, target_id, weapon_id, body_part_id, armour_id, damage):
        self.attacker_id = attacker_id
        self.target_id = target_id
        self.weapon_id = weapon_id
        self.body_part_id = body_part_id
        self.armour_id = armour_id
        self.damage = damage


class AttackMissedEvent:
    def __init__(self, attacker_id, target_id, weapon_id):
        self.attacker_id = attacker_id
        self.target_id = target_id
        self.weapon_id = weapon_id


class DiedEvent:
    def __init__(self, character_id):
        self.character_id = character_id


class TurnEndedEvent:

    def __init__(self, character_id):
        self.character_id = character_id
