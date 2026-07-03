def pig_latin(word: str) -> str:
    return f"{word}way" if word[0] in "aeiou" else f"{word[1:]}{word[0]}ay"


def pl_sentence(sentence: str) -> str:
    words = sentence.split()
    pig_sentence = [pig_latin(word) for word in words]
    return " ".join(pig_sentence)


if __name__ == "__main__":
    assert (
        pl_sentence("this is a test translation")
        == "histay isway away esttay ranslationtay"
    )
