import modules.Wordle as Wordle
import modules.SpellingBee as SpellingBee
import modules.ManageData as ManageData
from modules.ColourCodes import Colours
import signal
import sys
import time

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
    6) Quit
    {RESET}""")

def init_wordle() -> None:
    print(f"{BLUE}Type '-1' to quit.{RESET}")
    Wordle.init()

def init_spelling_bee() -> None:
    print(f"{BLUE}Type '-1' to quit.{RESET}")
    SpellingBee.init()

def show_scores() -> None:
    data = ManageData.get_user_data()
    if not data:
        print(f"{RED}[ERROR] Failed to load user scores.{RESET}")
        return
    
    spelling_bee_data = data["spelling_bee"]
    wordle_data = data["wordle"]

    spelling_bee_most_recent_score = spelling_bee_data["most_recent_score"]
    spelling_bee_past_scores = spelling_bee_data["past_scores"]
    spelling_bee_average = "N/A"

    if len(spelling_bee_past_scores) != 0:
        spelling_bee_average = round(sum([int(score) for score in spelling_bee_past_scores]) / len(spelling_bee_past_scores), 2)

    print(f"{GREEN}Spelling Bee:{RESET}")
    print(f"{GREEN}   - Average Score: {spelling_bee_average}")
    print(f"{GREEN}   - Most Recent Score: {spelling_bee_most_recent_score or "N/A"}")

    wordle_most_recent_score = wordle_data["most_recent_score"]
    wordle_past_scores = wordle_data["past_scores"]
    wordle_average = "N/A"

    if len(wordle_past_scores) != 0:
        wordle_average = round(sum([int(score) for score in wordle_past_scores]) / len(wordle_past_scores), 2)

    print(f"{GREEN}Wordle:{RESET}")
    print(f"{GREEN}   - Average Score (If user fails, score is set to seven by default): {wordle_average}")
    print(f"{GREEN}   - Most Recent Score: {wordle_most_recent_score or "N/A"}")

    input(f"{GREEN}\nPress 'return' to continue.{RESET}")

def create_wordle_game() -> None:
    print(f"{BLUE}Type '-1' to quit.{RESET}")
    Wordle.create_wordle_game()

def play_custom_wordle_game() -> None:
    print(f"{BLUE}Type '-1' to quit.{RESET}")
    Wordle.play_custom_wordle_game()

def quit_like_a_loser(*_) -> None:
    print(f"{RED}Quit you stupid quitter.{RESET}")
    sys.exit(0)

def get_user_choice() -> None:
    user_input = input(f"{BLUE}> {RESET}")
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
            quit_like_a_loser()
        case _:
            print(f"{RED}[ERROR] User is an idiot.{RESET}")
            input(f"{RED}Press 'return' to continue.{RESET}")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_like_a_loser)

    while True:
        load_menu()
        get_user_choice()