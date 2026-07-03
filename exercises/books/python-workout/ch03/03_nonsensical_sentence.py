def nonsensical_sentence(filename="fiction.txt", stop=10):
    sentence = []

    with open(filename, encoding="utf-8") as f:
        for n, line in enumerate(f, start=1):
            if n > stop:
                break

            words = line.split()
            if len(words) < n:
                raise ValueError(f"Line {n} has fewer than {n} words")
            sentence.append(words[n - 1])

    return " ".join(sentence)


if __name__ == "__main__":
    assert (
        nonsensical_sentence()
        == "The programmer evenings appeared engineers develops delete repeatedly was computers"
    )
