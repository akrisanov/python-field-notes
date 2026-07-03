from time import time


def gen_filename():
    i = 1

    while True:
        print(f"The generator has been called {i} time(s).")

        pattern = "file-{}.jpeg"
        t = int(time() * 1000)

        yield pattern.format(str(t))

        i += 1  # this line will be executed after the first yield call


def lettergen(s):
    """Yield letter by letter from a string."""
    for letter in s:
        # by calling yield, we switch the execution to the point
        # were the next() function is called
        yield letter


def numgen(n):
    """Yield number by number from a range."""
    for i in range(n):
        yield i


g1 = lettergen("Andrey")
g2 = numgen(4)

tasks = [g1, g2]

# yielding values from two generators in a round robin way
while tasks:
    task = tasks.pop(0)

    try:
        i = next(task)
        print(i)
        tasks.append(task)
    except StopIteration:
        pass
