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
    valid_words = []
    with open(path, "r") as f:
        lines = f.readlines()
        for line in lines:
            word = line.strip().lower()
            if len(word) >= MINIMUM_WORD_LENGTH:
                valid_words.append(word)
    
    return valid_words

def _passes_checks(letter_set: set) -> bool:
    vowel_count = len(letter_set & VOWELS)

    if vowel_count < 2:
        return False
    
    return True

def _evaluate_letter_set(letter_set: set, words: list) -> dict | None:
    #print(letter_set)
    if not _passes_checks(letter_set):
        return None
    
    for letter in letter_set:
        valid_words = []

        for word in words:
            if not (letter in word):
                continue

            unqiue_letters = set(word)
            if unqiue_letters.issubset(letter_set):
                valid_words.append(word)
            
        if len(valid_words) >= MINIMUM_WORDS_THAT_CAN_BE_MADE:
            return {
                "letters": letter_set,
                "centre": letter,
                "valid_words": valid_words,
            }
    
    return None

def _sample_letter_set() -> set:
    return set(random.sample(ALPHABET, LETTERS))

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
    correct_guesses = []
    spelling_bee_set = _generate_spelling_bee()
    points = 0

    if not spelling_bee_set:
        print(f"{RED}[ERROR] Failed to load letters.{RESET}")
        return
    
    letters = spelling_bee_set["letters"]
    centre = spelling_bee_set["centre"]
    valid_words = spelling_bee_set["valid_words"]

    #print(valid_words)

    print(f"{GREEN}Letters: {", ".join([letter for letter in letters])}{RESET}")
    print(f"{GREEN}Centre Letter: {centre}{RESET}")
    print(f"{GREEN}Total Words to Find: {len(valid_words)}{RESET}")
    print("Guesses: ")
    print(f"{BLUE}> {RESET}", end="", flush=True)

    while True:
        user_input = sys.stdin.readline().strip()

        if user_input == "-1":
            AchievementHandler.quitter_achievement()
            success_score = ManageData.write_value("spelling_bee", "most_recent_score", f"{points}")
            success_past_scores = ManageData.update_past_scores("spelling_bee", f"{points}")

            if not success_past_scores or not success_score:
                print(f"{RED}[ERROR] Could not save score to file.{RESET}")

            break

        if user_input.lower() in valid_words and not (user_input.lower() in correct_guesses):
            points += len(user_input)
            correct_guesses.append(user_input.lower())

        guesses = f"Guesses: {", ".join(correct_guesses)}"
        terminal_width = shutil.get_terminal_size().columns
        lines_used = math.ceil(len(guesses) / terminal_width)

        for _ in range(0, lines_used + 1):
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")

        print(guesses)
        
        print(f"{BLUE}> {RESET}", end="", flush=True)

        if len(correct_guesses) == len(valid_words):
            print(f"{GREEN}You found all the words!{RESET}")
            
            success_score = ManageData.write_value("spelling_bee", "most_recent_score", f"{points}")
            success_past_scores = ManageData.update_past_scores("spelling_bee", f"{points}")

            if not success_past_scores or not success_score:
                print(f"{RED}[ERROR] Could not save score to file.{RESET}")

            break
