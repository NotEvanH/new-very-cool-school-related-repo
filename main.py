# A lot of modules
import modules.Wordle as Wordle
import modules.SpellingBee as SpellingBee
import modules.ManageData as ManageData
import modules.LoadingScreen as LoadingScreen
from modules.ColourCodes import Colours
import random
import signal
import sys
import os

# Colours. Colours are cool
RED = Colours["Red"]
BLUE = Colours["Blue"]
GREEN = Colours["Green"]
RESET = Colours["Reset"]

# As this function's name aptly suggests, it outputs the user's options in the form of a menu.
def load_menu() -> None:
    print(f"""{BLUE}
    1) Wordle
    2) Spelling Bee
    3) Show Scores
    4) Create your own Wordle
    5) Play Custom Wordle
    6) Clear Data
    7) Quit
    {RESET}""")

def init_wordle() -> None:
    print(f"{BLUE}Type '-1' to quit.{RESET}")
    Wordle.init()

def init_spelling_bee() -> None:
    print(f"{BLUE}Type '-1' to quit.{RESET}")
    SpellingBee.init()

def output_game_scores(game_name: str) -> None:
    data = ManageData.get_user_data() # Attempts to get user data from ManageData module.
    if not data: # Error handling for if data isn't loaded.
        print(f"{RED}[ERROR] Failed to load user scores.{RESET}") # Useful error print message.
        return # Returns the function to prevent later code running and causing runtime error.

    game_data = data[game_name] # Gets data based on game_name parameter
    past_scores = game_data["past_scores"] # Loads past scores which is a list.
    most_recent_score = game_data["most_recent_score"] # Loads most recent score
    average = round(sum([int(score) for score in past_scores]) / len(past_scores), 2) if len(past_scores) != 0 else "N/A" # Calculates the average of all past scores.

    formatted_game_name = game_name.replace("_", " ").title() # Formats the game_name parameter into title case to be displayed to the user's in a more understandable way

    # Outputs scores
    print(f"{GREEN}{formatted_game_name}:{RESET}")
    print(f"{GREEN} - Average: {average}")
    print(f"{GREEN} - Most Recent Score: {most_recent_score}")

    # Checks if "winstreak" is presented in game data (will only be present for Wordle) and outputs it if it exists
    if "winstreak" in game_data:
        print(f"{GREEN} - Current Winstreak: {game_data["winstreak"]}{RESET}")
        print(f"{GREEN} - Highest Winstreak: {game_data["highest_winstreak"]}{RESET}")

def show_scores() -> None:
    data = ManageData.get_user_data()
    if not data:
        print(f"{RED}[ERROR] Failed to load user scores.{RESET}")
        return
    
    # Calls output_game_scores function for both Spelling Bee and Wordle
    output_game_scores("spelling_bee")
    output_game_scores("wordle")

    # Basic input function that prompts the user to click return to continue. Program flow is stopped by the input function until the user clicks enter
    input(f"{GREEN}\nPress 'return' to continue.{RESET}")

def create_wordle_game() -> None:
    print(f"{BLUE}Type '-1' to quit.{RESET}")
    Wordle.create_wordle_game()

def play_custom_wordle_game() -> None:
    print(f"{BLUE}Type '-1' to quit.{RESET}")
    Wordle.play_custom_wordle_game()

def clear_scores() -> None:
    # Creates a Python dictionary replicating the default data stored in the user_data.json file
    default_data = {
        "spelling_bee": {
            "most_recent_score": "N/A", "past_scores": []
        },
        "wordle": {
            "most_recent_score": "N/A", "past_scores": [], "winstreak": 0, "highest_winstreak": 0
        }}

    # Writes the data to the user_data.json file
    success = ManageData.write_user_data(default_data)

    # Error managing for if data failed to write
    if success:
        print(f"{GREEN}Successfully cleared all past data. Wonder why you felt the need to do that? You musn't be very good at this.{RESET}")
    else:
        print(f"{RED}[ERROR] Failed to clear data{RESET}")

def quit_like_a_loser(*_) -> None:
    print(f"{RED}Quit you stupid quitter.{RESET}") # Give nice print message
    sys.exit(0) # Quit the program nicely (avoids ugly Keyboard Interrupt message)

def gon_easter_egg() -> None:
    os.system("cls" if os.name == "nt" else "clear") # Clears the screen
    print("gon ", end="", flush=True) # prints "gon"
    # Infinite loop so they have time to stare at the word "gon"
    while True:
        pass

# Functionailty for getting the user's choice
def get_user_choice() -> None:
    user_input = input(f"{BLUE}> {RESET}").strip() # Gets it here
    # All the possiblities
    match user_input:
        case "1":
            init_wordle()
        case "2":
            init_spelling_bee()
        case "3":
            show_scores()
        case "4":
            create_wordle_game()
        case "5":
            play_custom_wordle_game()
        case "6":
            clear_scores()
        case "7":
            quit_like_a_loser()
        case "gon":
            gon_easter_egg()
        case _:
            # Yells at 'em if they don't choose one of the above options
            print(f"{RED}[ERROR] User is an idiot.{RESET}")
            input(f"{RED}Press 'return' to continue.{RESET}")

# Main function for control program flow
def main() -> None:
    loading_messages = ["hello.", "by javelinwebdesigns.com", "proud supporter of GON", "welcome to my game.", "nyt replica", "cheating is bad.", "spelling bee kinda geeked."] # List of loading messages
    random_message = random.choice(loading_messages) # Selecting a random loading message
    LoadingScreen.loading_screen(random_message) # Creating the matrix-esque loading screen with that message
    
    # Loop of showing the user's the menu and asking them for their choice
    while True:
        load_menu()
        get_user_choice()

if __name__ == "__main__":
    # Using signal library to handing interrupt signals nicely with the aforementioned "quit_like_a_loser" function
    signal.signal(signal.SIGINT, quit_like_a_loser)

    # Call main function to handle program flow
    main()