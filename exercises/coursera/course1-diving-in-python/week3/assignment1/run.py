from solution import FileReader

if __name__ == "__main__":
    reader = FileReader("not_exist_file.txt")
    text = reader.read()
    assert text == ""

    with open("hello.txt", "w") as f:
        f.write("Hello, World!")

    reader = FileReader("hello.txt")
    text = reader.read()
    assert text == "Hello, World!"
