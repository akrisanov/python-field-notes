def hello():
    with open("hello.txt", "w") as f:
        f.write("Hello World!\n")


if __name__ == "__main__":
    hello()
