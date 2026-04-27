import random
import string
import sys
import shutil
import math
from modules.ColourCodes import Colours
import modules.ManageData as ManageData
import modules.AchievementHandler as AchievementHandler

RED = Colours["Red"]
BLUE = Colours["Blue"]
GREEN = Colours["Green"]
RESET = Colours["Reset"]

MINIMUM_WORDS_THAT_CAN_BE_MADE = 10
MINIMUM_WORD_LENGTH = 4
MAX_ATTEMPTS = 10000
LETTERS = 7

VOWELS = set("aeiou")
ALPHABET = string.ascii_lowercase

# INTERAL FUNCTIONS

def _load_words(path: str) -> list:
    # Collating list of words that are over the minimum word length
    valid_words = []
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            word = line.strip().lower()
            if len(word) >= MINIMUM_WORD_LENGTH:
                valid_words.append(word)
    
    return valid_words

def _passes_checks(letter_set: set) -> bool:
    vowel_count = len(letter_set & VOWELS) # Using intersection to get amount of unqiue vowels

    if vowel_count < 2: # Need at least two vowels to qualify as a valid set of letters
        return False
    
    return True

# Function for evaluating a letter set is good enough for the user to play
def _evaluate_letter_set(letter_set: set, words: list) -> dict | None:
    #print(letter_set)
    if not _passes_checks(letter_set):
        return None
    
    for letter in letter_set:
        valid_words = []

        # Loop through every valid word
        for word in words:
            if not (letter in word): # Since we need a centre letter, this check makes sure the current letter is included in the word
                continue

            unqiue_letters = set(word)
            if unqiue_letters.issubset(letter_set): # Then the program makes sure the letters in the word are a subset of the letters in proposed letter set
                valid_words.append(word) # If it is, it is appended to the valid_words list
            
        if len(valid_words) >= MINIMUM_WORDS_THAT_CAN_BE_MADE: # If the valid words found with this letter set meets the quota, a dictionary with relevant information is returned
            return {
                "letters": letter_set,
                "centre": letter,
                "valid_words": valid_words,
            }
    
    return None

def _sample_letter_set() -> set:
    return set(random.sample(ALPHABET, LETTERS)) # Get a set of random letters

# Generating letters for Spelling Bee
def _generate_spelling_bee() -> dict | None:
    words = _load_words("SpellingBeeWords.txt")
    for _ in range(0, MAX_ATTEMPTS):
        letter_set = _sample_letter_set()
        evaluation = _evaluate_letter_set(letter_set, words)
        if evaluation:
            return evaluation
    
    return None

# EXTERNAL FUNCTIONS

def init() -> None:
    correct_guesses = [] # Correct user guesses are store here
    spelling_bee_set = _generate_spelling_bee() # Attempt to get valid set of letters
    points = 0 # Create variable to store the points the user gets (one point for each correct letter in a word)

    # If the function was unable to generate a valid set of words (statisically unlikly albeit a possibility), an error message is shown, and the function returns.
    if not spelling_bee_set:
        print(f"{RED}[ERROR] Failed to load letters.{RESET}")
        return
    
    # From the returned dictionary, the program pulls out the letters, the centre letter, and the valid words that could be made.
    letters = spelling_bee_set["letters"]
    centre = spelling_bee_set["centre"]
    valid_words = spelling_bee_set["valid_words"]

    #print(valid_words)

    # Display this information to the users
    print(f"{GREEN}Letters: {", ".join([letter for letter in letters])}{RESET}")
    print(f"{GREEN}Centre Letter: {centre}{RESET}")
    print(f"{GREEN}Total Words to Find: {len(valid_words)}{RESET}")
    print("Guesses: ")
    print(f"{BLUE}> {RESET}", end="", flush=True)

    while True:
        # User input is handled by sys instead of input() so the program can control newlines
        user_input = sys.stdin.readline().strip()

        if user_input == "-1":
            AchievementHandler.quitter_achievement()
            success_score = ManageData.write_value("spelling_bee", "most_recent_score", f"{points}")
            success_past_scores = ManageData.update_past_scores("spelling_bee", f"{points}")

            if not success_past_scores or not success_score:
                print(f"{RED}[ERROR] Could not save score to file.{RESET}")

            break
        
        # If the user's input was in valid_words, they guessed a correct word. Therefore, they get pointss
        if user_input.lower() in valid_words and not (user_input.lower() in correct_guesses):
            points += len(user_input)
            correct_guesses.append(user_input.lower())

        guesses = f"Guesses: {", ".join(correct_guesses)}"

        # Calculate the lines used by the guesses output
        terminal_width = shutil.get_terminal_size().columns
        lines_used = math.ceil(len(guesses) / terminal_width)

        # Program using ANSI codes to move back to the same line (prevents newlines because ugly)
        for _ in range(0, lines_used + 1):
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")

        print(guesses) # Output the user's correct guesses thus far
        
        print(f"{BLUE}> {RESET}", end="", flush=True)

        # If the length of the user's correct guesses is equal to that of valid_words, the user has found all of the words
        if len(correct_guesses) == len(valid_words):
            print(f"{GREEN}You found all the words!{RESET}")
            
            success_score = ManageData.write_value("spelling_bee", "most_recent_score", f"{points}")
            success_past_scores = ManageData.update_past_scores("spelling_bee", f"{points}")

            if not success_past_scores or not success_score:
                print(f"{RED}[ERROR] Could not save score to file.{RESET}")

            break
