import string


def pig_latin(word: str) -> str:
    is_capitalized = word[0].isupper() and word[1:].islower()
    punctuation = ""

    if word[-1] in string.punctuation:
        punctuation = word[-1]
        word = word[:-1]

    if word[0].lower() in "aeiou":
        pig_word = f"{word}way"
    else:
        pig_word = f"{word[1:]}{word[0]}ay"

    if is_capitalized:
        pig_word = pig_word[0].upper() + pig_word[1:].lower()

    return pig_word + punctuation


def pig_latin_alt(word: str) -> str:
    vowels = set(c for c in word if c in "aeiou")
    pig_word = f"{word}way" if len(vowels) >= 2 else f"{word[1:]}{word[0]}ay"
    return pig_word


if __name__ == "__main__":
    assert pig_latin("air") == "airway"
    assert pig_latin("eat") == "eatway"
    assert pig_latin("python") == "ythonpay"
    assert pig_latin("Python?") == "Ythonpay?"
    assert pig_latin("computer.") == "omputercay."
    assert pig_latin("Hello!") == "Ellohay!"

    assert pig_latin_alt("wine") == "wineway"
    assert pig_latin_alt("wind") == "indway"
