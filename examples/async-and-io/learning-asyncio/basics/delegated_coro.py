from unicodedata import name


def coroutine(func):
    """Initializes a generator eliminating g.send(None) call."""

    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g

    return inner


class CustomException(Exception):
    pass


# @coroutine
def subgen():
    while True:
        try:
            message = yield
        # except CustomException:
        except StopIteration:
            print("StopIteration is raised")
        else:
            print("...........", message)


@coroutine
def delegator(g):
    # while True:
    #     try:
    #         data = yield
    #         g.send(data)
    #     except CustomException as e:
    #         g.throw(e)
    # vs
    # NOTE: https://peps.python.org/pep-0380/
    yield from g


if __name__ == "__main__":
    g = subgen()
    d = delegator(g)
    g.send("OK")
    # g.throw(CustomException)
    g.throw(StopIteration)
