def grep(pattern):
    print("Start coroutine")
    try:
        while True:
            line = yield
            if pattern in line:
                print(line)
    except GeneratorExit:
        print("Stop coroutine")


g = grep("Python")
next(g)  # g.send(None)
g.send("Is Go better?")
# g.throw(RuntimeError, "boom!")
g.send("Python is not simple")
g.close()  # explicit close() method
