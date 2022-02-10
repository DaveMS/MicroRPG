from body_part import BodyPart
from body_part_type import BodyPartType
from anatomy import Anatomy
from natural_weapon_helpers import create_kick


def create_humanoid_anatomy(health_multiplier=1.0):
    return Anatomy([
        BodyPart(
            name="head",
            body_part_type=BodyPartType.head,
            health=10 * health_multiplier,
            chance_to_hit=0.12,
            loss_is_fatal=True,
            child_body_parts=[]
        ),
        BodyPart(
            name="neck",
            body_part_type=BodyPartType.neck,
            health=8 * health_multiplier,
            chance_to_hit=0.03,
            loss_is_fatal=True,
            child_body_parts=[]
        ),
        BodyPart("chest", BodyPartType.chest, 30 * health_multiplier, 0.30, True, None, [
            BodyPart("l. arm", BodyPartType.arm, 12 * health_multiplier, 0.10, None, child_body_parts=[
                BodyPart("l. hand", BodyPartType.hand, 5 * health_multiplier, 0.05, None, child_body_parts=[
                    BodyPart("l. finger 1", BodyPartType.finger, 2 * health_multiplier, 0.01),
                    BodyPart("l. finger 2", BodyPartType.finger, 2 * health_multiplier, 0.01),
                    BodyPart("l. finger 3", BodyPartType.finger, 2 * health_multiplier, 0.01),
                    BodyPart("l. finger 4", BodyPartType.finger, 2 * health_multiplier, 0.01),
                    BodyPart("l. finger 5", BodyPartType.finger, 2 * health_multiplier, 0.01),
                ])
            ]),
            BodyPart("r. arm", BodyPartType.arm, 12 * health_multiplier, 0.10, None, child_body_parts=[
                BodyPart("r. hand", BodyPartType.hand, 5 * health_multiplier, 0.05, None, child_body_parts=[
                    BodyPart("r. finger 1", BodyPartType.finger, 2 * health_multiplier, 0.01),
                    BodyPart("r. finger 2", BodyPartType.finger, 2 * health_multiplier, 0.01),
                    BodyPart("r. finger 3", BodyPartType.finger, 2 * health_multiplier, 0.01),
                    BodyPart("r. finger 4", BodyPartType.finger, 2 * health_multiplier, 0.01),
                    BodyPart("r. finger 5", BodyPartType.finger, 2 * health_multiplier, 0.01),
                ]),
            ]),
            BodyPart("l. leg", BodyPartType.leg, 20 * health_multiplier, 0.05, None, child_body_parts=[
                BodyPart("l. foot", BodyPartType.foot, 5 * health_multiplier, 0.025, natural_weapon=create_kick())
            ]),
            BodyPart("r. leg", BodyPartType.leg, 20 * health_multiplier, 0.05, child_body_parts=[
                BodyPart("r. foot", BodyPartType.foot, 5 * health_multiplier, 0.025, natural_weapon=create_kick())
            ])
        ]),

    ])
