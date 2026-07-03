import inspect


async def f():
    return 123


coro = f()
try:
    # When a coroutine returns, a StopIteration exception is raised:
    coro.send(None)
except StopIteration as e:
    print("The answer was:", e.value)
