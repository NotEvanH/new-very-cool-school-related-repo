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

CHARACTERS = string.ascii_lowercase + string.ascii_uppercase + string.punctuation

# INTERNAL FUNCTIONS

def _clear() -> None:
    os.system("cls" if os.name == "nt" else "clear") # Use an appropriate command to clear the terminal

# EXTERNAL FUNCTIONS

def loading_screen(message: str) -> None:
    message_x = (COLUMNS - len(message)) // 2 # Find where the message should start typing on the x-axis
    message_y = rows // 2 # Get the middle to type the message

    characters_loaded = 0
    
    for frame in range(40): # Forty frames
        output = [] # Store each line that should be loaded

        if frame % 3 == 0 and characters_loaded < len(message):
            characters_loaded += 1 # Load another character every three frames
        
        for y in range(rows): # Loop through each column
            line = ""
            for x in range(COLUMNS):
                if y == message_y and message_x <= x < message_x + len(message):
                    index = x - message_x # Figure out where letter should be loaded

                    # Load letter
                    if index < characters_loaded:
                        line += f"{GREEN}{message[index]}{RESET}"
                    else:
                        line += f"{GREEN}{random.choice(CHARACTERS)}{RESET}"
                else:
                    line += " "

            output.append(line) # Append new line to output list

        _clear() # Clear screen from past frame
        print("\n".join(output)) # Output stuff
        time.sleep(0.05) # Short visual pause

    output = []
    for y in range(rows):
        line = ""
        for x in range(COLUMNS):
            if y == message_y and message_x <= x < message_x + len(message):
                line += f"{GREEN}{message[x - message_x]}{RESET}"
            else:
                line += " "

        output.append(line)

    _clear() # Clear screen from past frame
    print("\n".join(output))  # Print final output

    time.sleep(1) # Pause for one second

    _clear() # Clear screen to load actual menu