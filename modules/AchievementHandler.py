from modules.ColourCodes import Colours
import json

RED = Colours["Red"]
GREEN = Colours["Green"]
RESET = Colours["Reset"]

FILEPATH = "achievements.json"

# INTERNAL FUNCTIONS

# Standard function to read achievements JSON file. Uses try-expect for good programming practice
def _read_json_file(filepath: str) -> dict:
    try:
        with open(filepath, "r") as f:
            return json.loads(f.read())
    except:
        print(f"{RED}[ERROR] Failed to load achievements file.{RESET}")
        return {}

# Standard function to write to achievements JSON file. Uses try-expect for good programming practice
def _write_json_file(filepath: str, new_data: dict) -> None:
    try:
        with open(filepath, "w") as f:
            f.write(
                json.dumps(new_data)
            )
    except:
        print(f"{RED}[ERROR] Failed to updated achievements file.{RESET}")

# EXTERNAL FUNCTIONS

# Iterating through JSON data and creating more user friendly list accomplished achievements
def get_achievements() -> list:
    data = _read_json_file(FILEPATH)
    if data:
        result = []
        for i, v in data.items():
            if v["achieved"]:
                result.append(i.replace("_", " ").title()) # In JSON, achievement is in snake case.
        
        return result
    
    return []

def update_achievements(states: list, user_guesses: list, won: bool) -> list:
    data = _read_json_file(FILEPATH)

    if not states:
        return []

    achievements = []

    # If every state is grey, then they've achieved Born Under An Unlucky Star
    if all([state == "grey" for state in states]) and not data["born_under_an_unlucky_star"]["achieved"]:
        achievements.append("Born Under An Unlucky Star")
    
    # Assuming the user has won, the program can check for other achievements
    if won:
        # If there were no yellow, green day has been won
        if all([state != "yellow" for state in states]) and not data["green_day"]["achieved"]:
            achievements.append("Green Day")
        
        # If the user won in a single guess, they can win luck of the draw
        if len(user_guesses) == 1 and not data["luck_of_the_draw"]["achieved"]:
            achievements.append("Luck Of The Draw")
        
        # If the user won in two guesses, they can win spare
        if len(user_guesses) == 2 and not data["spare"]["achieved"]:
            achievements.append("Spare")
        
    data = _read_json_file(FILEPATH)
    for achievement in achievements:
        data[achievement.replace(" ", "_").lower()]["achieved"] = True # Updating achievements in JSON file

    _write_json_file(FILEPATH, data)

    return achievements

# This function updates the quitter boy achievement and is called when a game is quitted
def quitter_achievement() -> None:
    new_data = _read_json_file(FILEPATH)
    if new_data:
        if not new_data["quitter_boy"]["achieved"]:
            new_data["quitter_boy"]["achieved"] = True

            _write_json_file(FILEPATH, new_data)
            print(f"{GREEN}Achievement Unlocked: Quitter Boy{RESET}")
            print(f"{GREEN} - {new_data["quitter_boy"]["description"]}{RESET}")