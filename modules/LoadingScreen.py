import time
import shutil
import random
import string
import os
from modules.ColourCodes import Colours

GREEN = Colours["Green"]
RESET = Colours["Reset"]

COLUMNS, rows = shutil.get_terminal_size()
rows -= 1
DROPS = [random.randint(0, rows) for _ in range(COLUMNS)]

CHARACTERS = string.ascii_lowercase + string.ascii_uppercase + string.punctuation

# INTERNAL FUNCTIONS

def _clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")

# EXTERNAL FUNCTIONS

def loading_screen(message: str) -> None:
    message_x = (COLUMNS - len(message)) // 2
    message_y = rows // 2

    characters_loaded = 0
    
    for frame in range(40):
        output = []

        if frame % 3 == 0 and characters_loaded < len(message):
            characters_loaded += 1
        
        for y in range(rows):
            line = ""
            for x in range(COLUMNS):
                if y == message_y and message_x <= x < message_x + len(message):
                    index = x - message_x

                    if index < characters_loaded:
                        line += f"{GREEN}{message[index]}{RESET}"
                    else:
                        line += f"{GREEN}{random.choice(CHARACTERS)}{RESET}"
                else:
                    line += " "

            output.append(line)

        _clear()
        print("\n".join(output))
        time.sleep(0.05)

    output = []
    for y in range(rows):
        line = ""
        for x in range(COLUMNS):
            if y == message_y and message_x <= x < message_x + len(message):
                line += f"{GREEN}{message[x - message_x]}{RESET}"
            else:
                line += " "

        output.append(line)

    _clear()
    print("\n".join(output))

    time.sleep(1)

    _clear()