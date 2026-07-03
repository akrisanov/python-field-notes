import random
import logging

logger = logging.getLogger(__name__)


def guessing_game(start=1, end=100, tries=3):
    answer = random.randint(start, end)
    base = random.randint(2, 16)
    guesses = 0

    logger.debug("The target number is %d", answer)

    print(f"I'm thinking of a number between {start} and {end}")
    print(f"You have {tries} tries.")

    while guesses < tries:
        try:
            guess_str = input(f"Enter your guess in base {base}: ").strip()
            guess = int(guess_str, base)
        except ValueError:
            print("Please enter a valid integer")
            continue
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            return

        guesses += 1

        if guess == answer:
            print("Just right")
            break

        if guess > answer:
            print("Too high")
        elif guess < answer:
            print("Too low")
    else:
        print("You didn't guess in time")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    guessing_game()
