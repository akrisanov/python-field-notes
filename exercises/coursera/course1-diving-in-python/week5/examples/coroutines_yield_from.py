def grep(pattern):
    print("Start coroutine")
    try:
        while True:
            line = yield
            if pattern in line:
                print(line)
    except GeneratorExit:
        print("Stop coroutine")


def grep_python():
    g = grep("Python")
    yield from g


g = grep_python()  # generator
next(g)
g.send("Is Go better?")
g.send("Python is not simple")
