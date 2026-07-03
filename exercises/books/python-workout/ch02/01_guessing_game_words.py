import random
import logging

logger = logging.getLogger(__name__)

WORDS = [
    "ant",
    "apple",
    "bat",
    "bear",
    "cat",
    "dog",
    "duck",
    "egg",
    "fish",
    "goat",
]


def guessing_game(tries: int = 3) -> None:
    answer_word = random.choice(WORDS)
    guesses = 0

    logger.debug("The target word is %s", answer_word)

    print(f"I'm thinking of a word from the following dictionary:\n{', '.join(WORDS)}")
    print(f"You have {tries} tries.")

    while guesses < tries:
        try:
            guess_word = input("Enter your guess: ").strip().casefold()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            return

        if guess_word not in WORDS:
            print("Not in the dictionary. Try one of the listed words.")
            continue

        guesses += 1

        if guess_word == answer_word:
            print("Just right")
            return
        elif guess_word > answer_word:
            print("Guess an earlier word")
        else:
            print("Guess a later word")

    print("You didn't guess in time")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    guessing_game()
