def coroutine(func):
    """Initializes a generator eliminating g.send(None) call."""

    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g

    return inner


def subgen():
    """Example:

    ```python
    g = subgen()
    g.send(None)
    g.send("hello")
    ```
    """
    reply = "Ready to accept message"
    message = yield reply
    print("Subgen received:", message)


class CustomException(Exception):
    pass


@coroutine
def average():
    """
    Calculate an average of some list of numbers.
    *Yield* the result.
    """
    count = 0
    sum = 0
    average = None

    while True:
        try:
            x = yield average
        except StopIteration:  # <- g.throw(StopIteration)
            print("Done")
        except CustomException:  # <- g.throw(CustomException)
            pass
        else:
            count += 1
            sum += x
            average = round(sum / count, 2)


@coroutine
def average2():
    """
    Calculate an average of some list of numbers.
    *Return*  the result when generator is exhausted.

    Example:
    ```python
    g = average2()
    g.send(1)
    g.send(3)

    try:
        g.throw(StopIteration)
    except StopIteration as e:
        print(f"Result is equal to {e.value}")
    ```
    """
    count = 0
    sum = 0
    average = None

    while True:
        try:
            x = yield
        except StopIteration:
            break
        except CustomException:
            break
        else:
            count += 1
            sum += x
            average = round(sum / count, 2)

    return average
