import random
import base64
import zlib
import json
import modules.ManageData as ManageData
import modules.AchievementHandler as AchievementHandler
from modules.ColourCodes import Colours

random_word = None # Randomly selected Wordle word will be assigned to this global variable. I wasn't allowed to use a class here, but if I could I would
user_guesses = [] # This list will be updated with the user's guesses each round
guesses = 6 # Dictates how many guesses the user is given. In a typically Wordle game, that's six guesses

# Yay! Colours.
RED = Colours["Red"]
BLUE = Colours["Blue"]
GREEN = Colours["Green"]
WORDLE_GREEN = Colours["WordleGreen"]
WORDLE_GREY = Colours["WordleGrey"]
WORDLE_YELLOW = Colours["WordleYellow"]
KEYBOARD_DARK_GREY = Colours["KeyboardDarkGrey"]
RESET = Colours["Reset"]

VALID_WORD_LIST_PATH = "ValidWords.txt" # File path to the list housing all the valid Wordle words (externally sourced)
SECRET_KEY = "hehesecretcode" # Secret code for generating custom Wordle games with xor function
KEYBOARD_LAYOUT = ["qwertyuiop↩", "asdfghjkl", "zxcvbnm"] # Keyboard layout where each string is an individual line on a typical keyboard

BEST_STARTER_WORD = "trace" # For Wordle bot's reference, this is the word it will always guess first

# INTERAL FUNCTIONS

# Function for handling Wordle bot
def _init_wordle_bot(valid_words: list) -> None:
    lines = [[""] * 5 for _ in range(0, 6)] # Creates an empty board using lists
    bot_win = False # Variable to store whether the bot has won the game
    bot_best_guess = BEST_STARTER_WORD # Creates a variable that stores the bot's best guess for that round
    past_bot_guesses = [BEST_STARTER_WORD] # A list of the bot's past guesses to avoid it guessing words it already knows are incorrect

    for i in range(0, guesses):
        # If statement to check if the user had already completed the Wordle or not. Done through comparing the round the bot is currently up to with the length of the list storing all of the user's guesses
        if i < len(user_guesses):
            # If the user was still playing in this round, their guess will also be outputted
            guess = user_guesses[i]
            print(f"{GREEN}Guess {i + 1}: You played {guess}{RESET}")
        else:
            # Alternatively, the program will just simply say they have already finished
            print(f"{GREEN}You'd already finished.{RESET}")

        # The program prints that the bot would have played that round
        print(f"{GREEN}Bot would have played {bot_best_guess}{RESET}")
        
        # Generates a Wordle board based on this information using the generate_wordle_board function
        lines[i] = list(bot_best_guess)
        generate_wordle_board(lines, random_word, {})
        
        # If the bot's guess was equal to the randomly selected word, then the bot has won, and the loop can be broken
        if bot_best_guess == random_word:
            bot_win = True
            print(f"{GREEN}Bot completed Wordle in {i + 1} guesses.{RESET}")
            input(f"{BLUE}Press 'enter' to return to main menu.{RESET}")

            break
        
        result, _ = get_letter_colours(lines[i], random_word, {}) # Calls get_letter_colours function to get list showing the 'colour' of each letter.
        possiblities = [] # Creates a list where all of the bot's possible guesses will be stored

        # Loops through every valid word to see if it's meets the bot's critera of a word is should play
        for word in valid_words:
            meets_criteria = True # Init a variable which is set to True by default. If the word doesn't meet any of the bot's requirements, this variable will be set to False
            
            if word in past_bot_guesses: # If the word is in the past_bot_guesses list, then it is invalid because the bot has already played it before
                meets_criteria = False
            
            for idx in range(5):
                letter = lines[i][idx] # Gets the letter at that certain index
                colour = result[idx] # Gets the colour of that letter

                if colour == "green":
                    # If the colour was green, and the letter that was green doesn't exist in the word from this iteration, it is invalid
                    if word[idx] != letter:
                        meets_criteria = False
                        break
                elif colour == "yellow":
                    # If the colour was yellow, and the letter in either not in the word or is in the right position, it is also invalid
                    if not (letter in word) or word[idx] == letter:
                        meets_criteria = False
                        break
                elif colour == "grey":
                    # If the colour was grey, and that letter exists in the word, then it is invalid
                    if letter in word:
                        meets_criteria = False
                        break
            
            # If the meets_criteria variable is still True after passing through the checks, it is added to the bot's list of possiblities
            if meets_criteria:
                possiblities.append(word)
        
        # If there were no possibilities (which should only happens if the code bugs, but it can (and most likely will) happen), then a random word is selected from the whole valid_words list
        if len(possiblities) == 0:
            bot_best_guess = random.choice(valid_words)
        else:
            bot_best_guess = random.choice(possiblities) # Alternatively, the bot selects a random word from the list of possiblities
        
        past_bot_guesses.append(bot_best_guess) # The bot's new guess will now be append to the bot's past guesses list
            
        input(f"{BLUE}Continue?{RESET}")
    
    if not bot_win: # If the bot did not win, the following prints are outputted
        print(f"{RED}Bot failed to complete Wordle.{RESET}")
        input(f"{BLUE}Press 'enter' to return to main menu.{RESET}")

def _load_keyboard(letter_states: dict) -> None:
    # Loops through each layer of the previously declared keyboard layout
    for i, layer in enumerate(KEYBOARD_LAYOUT):
        print(i * " ", end="") # Prints some ornamentary spaces to make the keyboard look indented like a real keyboard

        # Loops through each letter in the layer of letters to change their colour based on the user's prior guesses
        for letter in layer:
            letter_state = None
            if letter in letter_states:
                letter_state = letter_states[letter] # Configure letter_states based on user guesses

            print(
                f"{"".join(
                    [f"""{f"{WORDLE_GREEN}{letter}{RESET}" if letter_state == "green" else f"{WORDLE_YELLOW}{letter}{RESET}" if letter_state == "yellow" else f"{KEYBOARD_DARK_GREY}{letter}{RESET}" if letter_state == "grey" else f"{WORDLE_GREY}{letter}{RESET}"}"""]
                )}",
                end=""
            ) # Big print statement

        print() # Newline

def _load_words() -> list:
    try:
        with open(VALID_WORD_LIST_PATH, "r") as f:
            valid_words = f.readlines()
            valid_words = [word.strip() for word in valid_words] # Get valid words
        
        return valid_words
    except FileNotFoundError:
        print(f"{RED}[ERROR] File not found: resorting to default word{RESET}")
        valid_words = ["apple"] # Failsafe in case of error
        return valid_words

def _generate_random_word(valid_words: list) -> str:
    word = random.choice(valid_words) # Getting random word
    return word
    
def _make_guess(solution: str, guess: str) -> bool:
    return solution == guess # Pretty self-explainatory

def _xor(data: str, key: str):
    return bytes([letter ^ ord(key[i % len(key)]) for i, letter in enumerate(data)])

def _create_game_code(word: str):
    data = {"word": word} # Game data: current just a Python dictionary
    json_data = json.dumps(data).encode() # Make it JSON
    compressed_data = zlib.compress(json_data) # Compress it with built-in library zlib
    encrypted = _xor(compressed_data, SECRET_KEY) # Given it some basic encryption

    code = base64.urlsafe_b64encode(encrypted).decode() # Final Base64 encoded data that can be interpreted in the play_custom_wordle_game() function

    return code # Return code

# This is an important function
def _get_user_guesses(word: str, valid_words: list, is_custom_game: bool) -> tuple[bool, int]:
    lines = [[""] * 5 for _ in range(0, 6)] # Generate a Wordle board using Python lists
    letter_states = {} # Dictionary to store the states (i.e. colours) of letters in the user's guess

    generate_wordle_board(lines, word, letter_states) # Generate board
    _load_keyboard(letter_states) # Load keyboard

    can_use_hint = True # Guess this variable signifies? You'll never guess it.

    print(f"{GREEN}If you're in need of a hint, type '-2'. You get one hint per game.{RESET}")

    for round in range(0, guesses):
        user_input = None
        should_quit = False
        while user_input == None:
            try:
                user_input = input(f"{BLUE}Enter thine guess: {RESET}").lower() # Get user input
                    
                if user_input == "-2" and can_use_hint: # Gib them a hint if they can have one
                    can_use_hint = False
                    hint = _get_hint(word)
                    print(f"{GREEN}Revealed Letter: {hint}{RESET}")

                    user_input = input(f"{BLUE}Enter thine guess: {RESET}").lower()
                
                if user_input == "-2": # If they try to request another hint, decline them
                    raise Exception
                
                if user_input == "-1": # -1 is for when a user quits
                    AchievementHandler.quitter_achievement() # Give them the quitter achievement
                    should_quit = True
                    break # Break the loop

                if len(user_input) != 5: # If user input is more than five characters, raise a ValueError because that's no good in Wordle
                    raise ValueError
                
                if not is_custom_game and not (user_input in valid_words): # If the user input doesn't exist in the ValidWords.txt list, we decline them. This prevents inputs like "AEIOU" that could be used to discover letters.
                    raise ValueError
            # Below are polite, constructive error messages.
            except ValueError:
                user_input = None
                print(f"{RED}[ERROR] Ensure guess is five letters long and word is valid.{RESET}")
            except Exception:
                print(f"{RED}[ERROR] You've already used your hint.{RESET}")
                user_input = None

        if should_quit == True:
            break

        lines[round] = list(user_input) # Set round to the user's guess
        generate_wordle_board(lines, word, letter_states) # Show Wordle board
        _, letter_states = get_letter_colours(user_input, word, letter_states) # Get letter states
        _load_keyboard(letter_states) # Load keyboard again
        
        correct = _make_guess(word, user_input) # Check if the user's guess was correct
        user_guesses.append(user_input) # Add user's guess to the list of past guesses

        if correct:
            print(f"{GREEN}You win! The word was {word}.{RESET}") # If it was correct, the user wins. Yay!
            return True, round # Returns True to signify that the user won and the amount of rounds it took the user to win 
    
    return False, 7

def _get_hint(word: str) -> str:
    return random.choice(word) # Select a random letter in the word as a hint

# EXTERNAL FUNCTIONS

def generate_wordle_board(lines: list, word: str, letter_states: dict) -> None:
    for line in lines: # Loop through all lines
        if not any(line): # If there are no lines, print five dashes
            print("-----")
            continue
        
        result, _ = get_letter_colours(line, word, letter_states) # Get colours

        # Using ANSI colour codes to print each letter with its appropriate colour
        for i in range(0, 5):
            if result[i] == "green":
                print(f"{WORDLE_GREEN}{line[i]}{RESET}", end="")
            elif result[i] == "yellow":
                print(f"{WORDLE_YELLOW}{line[i]}{RESET}", end="")
            else:
                print(f"{WORDLE_GREY}{line[i]}{RESET}", end="")
        print() # New line

def get_letter_colours(line: list, word: str, letter_states: dict) -> tuple[list, dict]:
    result = [""] * 5 # Generate a list like this ["", "", "", "", ""]

    # Storing how many times each letter is included
    letter_count = {}
    for letter in word:
        if letter in letter_count:
            letter_count[letter] += 1
        else:
            letter_count[letter] = 1

    # Loop through each letter    
    for i in range(0, 5):
        if line[i] == word[i]: # If letters in the user's guess and the correct word align, it is green
            result[i] = "green"
            letter_count[line[i]] -= 1
            letter_states[line[i]] = "green"
        
    for i in range(0, 5):
        if result[i] == "":
            if line[i] in letter_count and letter_count[line[i]] > 0: # Alternatively, if the word includes the letter and it hasn't already been counter, it's yellow
                result[i] = "yellow"
                letter_count[line[i]] -= 1
                letter_states[line[i]] = "yellow"
            else: # Otherwise, it's grey
                result[i] = "grey"
                letter_states[line[i]] = "grey"
    
    return result, letter_states

def create_wordle_game() -> None:  
    custom_word = input(f"{BLUE}Enter your custom word: {RESET}")
    if custom_word == "-1":
        AchievementHandler.quitter_achievement()
        return
    
    # Ensures custom word is equal five characters
    while len(custom_word) != 5:
        print(f"{RED}[ERROR] Word must be at least five letters long.{RESET}")
        custom_word = input(f"{BLUE}Enter your custom word: {RESET}")
        if custom_word == "-1":
            AchievementHandler.quitter_achievement()
            return
    
    game_code = _create_game_code(custom_word)
    print(f"{GREEN}Share this code with your friends for them to play: {game_code}{RESET}") # Output code

def play_custom_wordle_game() -> None:
    valid_words = _load_words()
    print(f"{BLUE}Please note that custom games will award you no points.{RESET}")
    code = input(f"{BLUE}Enter enter the custom code: {RESET}")
    if code == "-1":
        AchievementHandler.quitter_achievement()
        return
    
    # Decode code to get word
    try:
        decoded_code = base64.urlsafe_b64decode(code)
        unencrypted_code = _xor(decoded_code, SECRET_KEY)
        decompressed = zlib.decompress(unencrypted_code).decode()
        decoded_code = json.loads(decompressed)
        word = decoded_code["word"]

        success = _get_user_guesses(word, valid_words, True) # Once decoded, game is player

        if not success:
            print(f"{RED}You lose! The word was {word}.{RESET}")
    except:
        print(f"{RED}[ERROR] Please enter a valid code.{RESET}") # Input validation

def init() -> None:
    global random_word
    global user_guesses

    valid_words = _load_words()
    random_word = _generate_random_word(valid_words)
    success, round = _get_user_guesses(random_word, valid_words, False)

    winstreak = ManageData.get_value("wordle", "winstreak")
    highest_winstreak = ManageData.get_value("wordle", "highest_winstreak")

    # Load letter states to be used by achievements function
    states = []
    for guess in user_guesses:
        _, letter_states = get_letter_colours(list(guess), random_word, {})
        for state in letter_states.values():
            states.append(state)

    # Let the user know if they accomplished any achievements
    achievements = AchievementHandler.update_achievements(states, user_guesses, success)
    data = AchievementHandler._read_json_file(AchievementHandler.FILEPATH)
    for achievement in achievements:
        print(f"{GREEN}Achievement Unlocked: {achievement}{RESET}")
        print(f"{GREEN} - {data[achievement.replace(" ", "_").lower()]["description"]}")

    # If user lost
    if not success:
        print(f"{RED}You lose! The word was {random_word}.{RESET}") # Tell them what the correct word would have been

        # Score set to seven upon failure (real NYTimes Games do this too)
        success_score = ManageData.write_value("wordle", "most_recent_score", "7")
        success_past_scores = ManageData.update_past_scores("wordle", "7")

        success_winstreak = ManageData.write_value("wordle", "winstreak", 0) # Winstreak reset

        if not success_past_scores or not success_score or not success_winstreak:
            print(f"{RED}[ERROR] Could not save score to file.{RESET}")

        if winstreak > highest_winstreak: # Check if current winstreak is greater than highest winstreak
            if not ManageData.write_value("wordle", "highest_winstreak", winstreak):
                print(f"{RED}[ERROR] Could not save score to file.{RESET}")
    else: # If the won
        success_score = ManageData.write_value("wordle", "most_recent_score", f"{round + 1}/6")
        success_past_scores = ManageData.update_past_scores("wordle", f"{round + 1}")
        success_winstreak = ManageData.write_value("wordle", "winstreak", winstreak + 1) # Increment winstreak

        if not success_past_scores or not success_score:
            print(f"{RED}[ERROR] Could not save score to file.{RESET}")
        
        if int(winstreak + 1) >= int(highest_winstreak): # Check if current winstreak is greater than highest winstreak
            if not ManageData.write_value("wordle", "highest_winstreak", winstreak + 1):
                print(f"{RED}[ERROR] Could not save score to file.{RESET}")
    
    # Wordle Bot
    do_wordle_bot = input(f"{BLUE}Did you beat the bot? Press 'b' to see. {RESET}").lower() == "b"
    if do_wordle_bot:
        _init_wordle_bot(valid_words)
    
    # Reset user_guesses variable to empty list for next game
    user_guesses = []
