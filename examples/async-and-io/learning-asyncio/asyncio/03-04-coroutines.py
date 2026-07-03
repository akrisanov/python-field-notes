import inspect


async def f():
    return 123


print(type(f))  # <class 'function'>
print(inspect.iscoroutinefunction(f))  # True

coro = f()
print(type(coro))  # <class 'coroutine'>
