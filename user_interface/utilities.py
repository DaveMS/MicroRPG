import re
import os


def get_user_input(prompt, allowed_values=[], print_allowed_values=True, allow_cancel=True, convert_to_lower=True):
    is_input_restricted = len(allowed_values) > 0

    if allow_cancel:
        allowed_values.append("(c)ancel")

    expanded_allowed_values = __expand_allowed_input_values(allowed_values)

    if print_allowed_values and allowed_values is not None:
        prompt += f"\n   " + " ".join(allowed_values)

    prompt += "\n :> "
    user_input = ""
    is_input_valid = False
    while not is_input_valid:
        user_input = input(prompt)
        if convert_to_lower:
            user_input = user_input.lower()
        is_input_valid = not is_input_restricted or user_input in expanded_allowed_values

    if allow_cancel and user_input in ("c", "cancel"):
        return False, ""
    return True, user_input


def __expand_allowed_input_values(allowed_inputs):
    return sum(map(lambda x: __split_allowed_value_input_into_value_and_hotkey(x), allowed_inputs), [])


def __split_allowed_value_input_into_value_and_hotkey(allowed_value):
    match = re.search("\(\w*\)", allowed_value)
    if match is None:
        return [allowed_value]
    hot_key = match.group()[1:-1]
    word_without_parenthesis = re.sub('[\(\)]', '', allowed_value)
    return [hot_key, word_without_parenthesis]


def select_character_target(characters):
    for i in range(len(characters)):
        print(f"{i}) {characters[i].name}")

    allowed_values = [str(i) for i in range(len(characters))]
    success, index_string = get_user_input(prompt="Select a target: ", print_allowed_values=False,
                                           allowed_values=allowed_values)
    if not success:
        return False, None
    return True, int(index_string)


def select_item(prompt, items):
    for i in range(len(items)):
        print(f"{i}) {items[i].name} weight: {items[i].weight}")
    print()

    allowed_values = [str(i) for i in range(len(items))]
    success, index_string = get_user_input(prompt=prompt, print_allowed_values=False, allowed_values=allowed_values)

    if not success:
        return False, None
    return (True, int(index_string))


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
