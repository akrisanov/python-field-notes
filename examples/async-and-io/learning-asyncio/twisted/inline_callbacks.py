from twisted import defer


@defer.inlineCallbacks
def f():
    yield
    # how you have to return values from @inlineCallbacks coroutines
    defer.returnValue(123)


@defer.inlineCallbacks
def my_coro_func():
    """For @inlineCallbacks to work, there must be at least one yield present
    in the function being decorated."""
    value = yield f()  # makes this function a generator
    assert value == 123
