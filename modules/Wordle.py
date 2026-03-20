import random
import base64
import zlib
import json
import modules.ManageData as ManageData
from modules.ColourCodes import Colours

random_word = None
guesses = 6

RED = Colours["Red"]
BLUE = Colours["Blue"]
GREEN = Colours["Green"]
WORDLE_GREEN = Colours["WordleGreen"]
WORDLE_GREY = Colours["WordleGrey"]
WORDLE_YELLOW = Colours["WordleYellow"]
KEYBOARD_DARK_GREY = Colours["KeyboardDarkGrey"]
RESET = Colours["Reset"]

VALID_WORD_LIST_PATH = "ValidWords.txt"
SECRET_KEY = "hehesecretcode"
KEYBOARD_LAYOUT = ["qwertyuiop↩", "asdfghjkl", "zxcvbnm"]

# INTERAL FUNCTIONS

def _load_keyboard(letter_states: dict) -> None:
    for i, layer in enumerate(KEYBOARD_LAYOUT):
        print(i * " ", end="")
        for letter in layer:
            letter_state = None
            if letter in letter_states:
                letter_state = letter_states[letter]

            print(
                f"{"".join(
                    [f"""{f"{WORDLE_GREEN}{letter}{RESET}" if letter_state == "green" else f"{WORDLE_YELLOW}{letter}{RESET}" if letter_state == "yellow" else f"{WORDLE_GREY}{letter}{RESET}" if letter_state == "grey" else f"{KEYBOARD_DARK_GREY}{letter}{RESET}"}"""]
                )}",
                end=""
            )

        print()

def _load_words() -> list:
    try:
        with open(VALID_WORD_LIST_PATH, "r") as f:
            valid_words = f.readlines()
            valid_words = [word.strip() for word in valid_words]
        
        return valid_words
    except FileNotFoundError:
        print(f"{RED}[ERROR] File not found: resorting to default word{RESET}")
        valid_words = ["apple"]
        return valid_words

def _generate_random_word(valid_words) -> str:
    word = random.choice(valid_words)
    return word
    
def _make_guess(solution: str, guess: str) -> bool:
    return solution == guess

def _generate_wordle_board(lines: list, word: str, letter_states: dict) -> None:
    for line in lines:
        if not any(line):
            print("-----")
            continue
        result = [""] * 5
        
        letter_count = {}
        for letter in word:
            if letter in letter_count:
                letter_count[letter] += 1
            else:
                letter_count[letter] = 1
        
        for i in range(0, 5):
            if line[i] == word[i]:
                result[i] = "green"
                letter_count[line[i]] -= 1
                letter_states[line[i]] = "green"
        
        for i in range(0, 5):
            if result[i] == "":
                if line[i] in letter_count and letter_count[line[i]] > 0:
                    result[i] = "yellow"
                    letter_count[line[i]] -= 1
                    letter_states[line[i]] = "yellow"
                else:
                    result[i] = "grey"
                    letter_states[line[i]] = "grey"

        for i in range(0, 5):
            if result[i] == "green":
                print(f"{WORDLE_GREEN}{line[i]}{RESET}", end="")
            elif result[i] == "yellow":
                print(f"{WORDLE_YELLOW}{line[i]}{RESET}", end="")
            else:
                print(f"{WORDLE_GREY}{line[i]}{RESET}", end="")
        print()
    return letter_states

def _xor(data: str, key: str):
    return bytes([letter ^ ord(key[i % len(key)]) for i, letter in enumerate(data)])

def _create_game_code(word: str):
    data = {"word": word}
    json_data = json.dumps(data).encode()
    compressed_data = zlib.compress(json_data)
    encrypted = _xor(compressed_data, SECRET_KEY)

    code = base64.urlsafe_b64encode(encrypted).decode()

    return code

def _get_user_guess(word: str) -> tuple[bool, int]:
    lines = [["", "", "", "", "", ""] for _ in range(0, 6)]
    letter_states = {}

    _generate_wordle_board(lines, word, letter_states)
    _load_keyboard(letter_states)

    for round in range(0, guesses):
        user_input = None
        should_quit = False
        while user_input == None:
            try:
                user_input = input(f"{BLUE}Enter thine guess: {RESET}").lower()
                
                if user_input == "-1":
                    should_quit = True
                    break

                if len(user_input) != 5:
                    raise ValueError
            except ValueError:
                user_input = None
                print(f"{RED}[ERROR] Ensure guess is five letters long.{RESET}")

        if should_quit == True:
            break

        lines[round] = list(user_input)
        letter_states = _generate_wordle_board(lines, word, letter_states)
        _load_keyboard(letter_states)
        
        corrent = _make_guess(word, user_input)

        if corrent:
            print(f"{GREEN}You win! The word was {word}.{RESET}")
            return True, round
    
    return False, 7

# EXTERNAL FUNCTIONS

def create_wordle_game() -> None:  
    custom_word = input(f"{BLUE}Enter your custom word: {RESET}")
    if custom_word == "-1":
            return
    
    while len(custom_word) != 5:
        print(f"{RED}[ERROR] Word must be at least five letters long.{RESET}")
        custom_word = input(f"{BLUE}Enter your custom word: {RESET}")
        if custom_word == "-1":
            return
    
    game_code = _create_game_code(custom_word)
    print(f"{GREEN}Share this code with your friends for them to play: {game_code}{RESET}")

def play_custom_wordle_game() -> None:
    print(f"{BLUE}Please note that custom games will award you no points.{RESET}")
    code = input(f"{BLUE}Enter enter the custom code: {RESET}")
    if code == "-1":
        return
    
    try:
        decoded_code = base64.urlsafe_b64decode(code)
        unencrypted_code = _xor(decoded_code, SECRET_KEY)
        decompressed = zlib.decompress(unencrypted_code).decode()
        decoded_code = json.loads(decompressed)
    except:
        print(f"{RED}[ERROR] Please enter a valid code.{RESET}")

    word = decoded_code["word"]
    success = _get_user_guess(word)

    if not success:
        print(f"{RED}You lose! The word was {random_word}.{RESET}")

def init() -> None:
    global random_word
    valid_words = _load_words()
    random_word = _generate_random_word(valid_words)
    #print(random_word)
    success, round = _get_user_guess(random_word)

    if not success:
        print(f"{RED}You lose! The word was {random_word}.{RESET}")
        success_score = ManageData.write_value("wordle", "most_recent_score", "7")
        success_past_scores = ManageData.update_past_scores("wordle", "7")

        if not success_past_scores or not success_score:
            print(f"{RED}[ERROR] Could not save score to file.{RESET}")
    else:
        success_score = ManageData.write_value("wordle", "most_recent_score", f"{round + 1}/6")
        success_past_scores = ManageData.update_past_scores("wordle", f"{round + 1}")

        if not success_past_scores or not success_score:
            print(f"{RED}[ERROR] Could not save score to file.{RESET}")
