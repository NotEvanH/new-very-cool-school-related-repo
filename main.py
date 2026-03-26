import modules.Wordle as Wordle
import modules.SpellingBee as SpellingBee
import modules.ManageData as ManageData
import modules.LoadingScreen as LoadingScreen
from modules.ColourCodes import Colours
import random
import signal
import sys
import os

RED = Colours["Red"]
BLUE = Colours["Blue"]
GREEN = Colours["Green"]
RESET = Colours["Reset"]

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
    data = ManageData.get_user_data()
    if not data:
        print(f"{RED}[ERROR] Failed to load user scores.{RESET}")
        return

    game_data = data[game_name]
    past_scores = game_data["past_scores"]
    most_recent_score = game_data["most_recent_score"]
    average = round(sum([int(score) for score in past_scores]) / len(past_scores), 2) if len(past_scores) != 0 else "N/A"

    formatted_game_name = game_name.replace("_", " ").title()

    print(f"{GREEN}{formatted_game_name}:{RESET}")
    print(f"{GREEN} - Average: {average}")
    print(f"{GREEN} - Most Recent Score: {most_recent_score}")

    if "winstreak" in game_data:
        print(f"{GREEN} - Current Winstreak: {game_data["winstreak"]}{RESET}")
        print(f"{GREEN} - Highest Winstreak: {game_data["highest_winstreak"]}{RESET}")

def show_scores() -> None:
    data = ManageData.get_user_data()
    if not data:
        print(f"{RED}[ERROR] Failed to load user scores.{RESET}")
        return
    
    output_game_scores("spelling_bee")
    output_game_scores("wordle")

    input(f"{GREEN}\nPress 'return' to continue.{RESET}")

def create_wordle_game() -> None:
    print(f"{BLUE}Type '-1' to quit.{RESET}")
    Wordle.create_wordle_game()

def play_custom_wordle_game() -> None:
    print(f"{BLUE}Type '-1' to quit.{RESET}")
    Wordle.play_custom_wordle_game()

def clear_scores() -> None:
    default_data = {
        "spelling_bee": {
            "most_recent_score": "N/A", "past_scores": []
        },
        "wordle": {
            "most_recent_score": "N/A", "past_scores": [], "winstreak": 0, "highest_winstreak": 0
        }}

    success = ManageData.write_user_data(default_data)
    if success:
        print(f"{GREEN}Successfully cleared all past data. Wonder why you felt the need to do that? You musn't be very good at this.{RESET}")
    else:
        print(f"{RED}[ERROR] Failed to clear data{RESET}")

def quit_like_a_loser(*_) -> None:
    print(f"{RED}Quit you stupid quitter.{RESET}")
    sys.exit(0)

def gon_easter_egg() -> None:
    os.system("cls" if os.name == "nt" else "clear")
    print("gon ", end="", flush=True)
    while True:
        pass

def get_user_choice() -> None:
    user_input = input(f"{BLUE}> {RESET}").strip()
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
            print(f"{RED}[ERROR] User is an idiot.{RESET}")
            input(f"{RED}Press 'return' to continue.{RESET}")

def main() -> None:
    loading_messages = ["hello.", "by javelinwebdesigns.com", "proud supporter of GON", "welcome to my game.", "nyt replica", "cheating is bad.", "spelling bee kinda geeked."]
    random_message = random.choice(loading_messages)
    LoadingScreen.loading_screen(random_message)
    
    while True:
        load_menu()
        get_user_choice()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_like_a_loser)
    main()