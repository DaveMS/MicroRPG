import random


class DiceRoll:

    def __init__(self, num_dice, sides):
        self.num_dice = num_dice
        self.num_sides = sides

    def roll(self):
        total = 0
        for i in range(self.num_dice):
            dice_roll_complete = False
            while not dice_roll_complete:
                roll = random.randint(1, self.num_sides)
                total += roll
                dice_roll_complete = roll is not self.num_sides
                if not dice_roll_complete:
                    total -= 1
        return total
