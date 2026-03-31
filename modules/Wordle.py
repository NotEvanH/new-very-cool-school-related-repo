import random
import base64
import zlib
import json
import modules.ManageData as ManageData
from modules.ColourCodes import Colours

random_word = None
user_guesses = []
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

BEST_STARTER_WORD = "trace"

# INTERAL FUNCTIONS

def _init_wordle_bot(valid_words: list) -> None:
    lines = [[""] * 5 for _ in range(0, 6)]
    bot_win = False
    bot_best_guess = BEST_STARTER_WORD
    past_bot_guesses = [BEST_STARTER_WORD]
    for i in range(0, 6):
        if i < len(user_guesses):
            guess = user_guesses[i]
            print(f"{GREEN}Guess {i + 1}: You played {guess}{RESET}")
        else:
            print(f"{GREEN}You'd already finished.{RESET}")

        print(f"{GREEN}Bot would have played {bot_best_guess}{RESET}")
        lines[i] = list(bot_best_guess)
        generate_wordle_board(lines, random_word, {})
        
        if bot_best_guess == random_word:
            bot_win = True
            print(f"{GREEN}Bot completed Wordle in {i + 1} guesses.{RESET}")
            input(f"{BLUE}Press 'enter' to return to main menu.{RESET}")

            break
        
        result, _ = get_letter_colours(lines[i], random_word, {})
        possiblities = []

        for word in valid_words:
            meets_criteria = True
            
            if word in past_bot_guesses:
                meets_criteria = False

            for idx in range(5):
                letter = lines[i][idx]
                colour = result[idx]

                if colour == "green":
                    if word[idx] != letter:
                        meets_criteria = False
                        break
                elif colour == "yellow":
                    if not (letter in word) or word[idx] == letter:
                        meets_criteria = False
                        break
                elif colour == "grey":
                    if letter in word:
                        meets_criteria = False
                        break
            
            if meets_criteria:
                possiblities.append(word)
        
        if len(possiblities) == 0:
            bot_best_guess = random.choice(valid_words)
        else:
            bot_best_guess = random.choice(possiblities)
        
        past_bot_guesses.append(bot_best_guess)
            
        input(f"{BLUE}Continue?{RESET}")
    
    if not bot_win:
        print(f"{RED}Bot failed to complete Wordle.{RESET}")
        input(f"{BLUE}Press 'enter' to return to main menu.{RESET}")

def _load_keyboard(letter_states: dict) -> None:
    for i, layer in enumerate(KEYBOARD_LAYOUT):
        print(i * " ", end="")
        for letter in layer:
            letter_state = None
            if letter in letter_states:
                letter_state = letter_states[letter]

            print(
                f"{"".join(
                    [f"""{f"{WORDLE_GREEN}{letter}{RESET}" if letter_state == "green" else f"{WORDLE_YELLOW}{letter}{RESET}" if letter_state == "yellow" else f"{KEYBOARD_DARK_GREY}{letter}{RESET}" if letter_state == "grey" else f"{WORDLE_GREY}{letter}{RESET}"}"""]
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

def _generate_random_word(valid_words: list) -> str:
    word = random.choice(valid_words)
    return word
    
def _make_guess(solution: str, guess: str) -> bool:
    return solution == guess

def _xor(data: str, key: str):
    return bytes([letter ^ ord(key[i % len(key)]) for i, letter in enumerate(data)])

def _create_game_code(word: str):
    data = {"word": word}
    json_data = json.dumps(data).encode()
    compressed_data = zlib.compress(json_data)
    encrypted = _xor(compressed_data, SECRET_KEY)

    code = base64.urlsafe_b64encode(encrypted).decode()

    return code

def _get_user_guesses(word: str, valid_words: list, is_custom_game: bool) -> tuple[bool, int]:
    lines = [[""] * 5 for _ in range(0, 6)]
    letter_states = {}

    generate_wordle_board(lines, word, letter_states)
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
                
                if not is_custom_game and not (user_input in valid_words):
                    raise ValueError
            except ValueError:
                user_input = None
                print(f"{RED}[ERROR] Ensure guess is five letters long and word is valid.{RESET}")

        if should_quit == True:
            break

        lines[round] = list(user_input)
        generate_wordle_board(lines, word, letter_states)
        _, letter_states = get_letter_colours(user_input, word, letter_states)
        _load_keyboard(letter_states)
        
        correct = _make_guess(word, user_input)
        user_guesses.append(user_input)

        if correct:
            print(f"{GREEN}You win! The word was {word}.{RESET}")
            return True, round
    
    return False, 7

# EXTERNAL FUNCTIONS

def generate_wordle_board(lines: list, word: str, letter_states: dict) -> None:
    for line in lines:
        if not any(line):
            print("-----")
            continue
        
        result, _ = get_letter_colours(line, word, letter_states)

        for i in range(0, 5):
            if result[i] == "green":
                print(f"{WORDLE_GREEN}{line[i]}{RESET}", end="")
            elif result[i] == "yellow":
                print(f"{WORDLE_YELLOW}{line[i]}{RESET}", end="")
            else:
                print(f"{WORDLE_GREY}{line[i]}{RESET}", end="")
        print()

def get_letter_colours(line: list, word: str, letter_states: dict) -> tuple[list, dict]:
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
    
    return result, letter_states

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
    valid_words = _load_words()
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
    success = _get_user_guesses(word, valid_words, True)

    if not success:
        print(f"{RED}You lose! The word was {word}.{RESET}")

def init() -> None:
    global random_word
    global user_guesses

    valid_words = _load_words()
    random_word = _generate_random_word(valid_words)   
    success, round = _get_user_guesses(random_word, valid_words, False)

    winstreak = ManageData.get_value("wordle", "winstreak")
    highest_winstreak = ManageData.get_value("wordle", "highest_winstreak")

    if not success:
        print(f"{RED}You lose! The word was {random_word}.{RESET}")
        success_score = ManageData.write_value("wordle", "most_recent_score", "7")
        success_past_scores = ManageData.update_past_scores("wordle", "7")
        success_winstreak = ManageData.write_value("wordle", "winstreak", 0)

        if not success_past_scores or not success_score or not success_winstreak:
            print(f"{RED}[ERROR] Could not save score to file.{RESET}")

        if winstreak > highest_winstreak:
            if not ManageData.write_value("wordle", "highest_winstreak", winstreak):
                print(f"{RED}[ERROR] Could not save score to file.{RESET}")
    else:
        success_score = ManageData.write_value("wordle", "most_recent_score", f"{round + 1}/6")
        success_past_scores = ManageData.update_past_scores("wordle", f"{round + 1}")
        success_winstreak = ManageData.write_value("wordle", "winstreak", winstreak + 1)

        if not success_past_scores or not success_score:
            print(f"{RED}[ERROR] Could not save score to file.{RESET}")
        
        if int(winstreak + 1) >= int(highest_winstreak):
            if not ManageData.write_value("wordle", "highest_winstreak", winstreak + 1):
                print(f"{RED}[ERROR] Could not save score to file.{RESET}")
    
    do_wordle_bot = input(f"{BLUE}Did you beat the bot? Press 'b' to see. {RESET}").lower() == "b"
    if do_wordle_bot:
        _init_wordle_bot(valid_words)
    
    user_guesses = []
