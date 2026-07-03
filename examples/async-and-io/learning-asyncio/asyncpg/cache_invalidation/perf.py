import logging
from time import perf_counter
from inspect import iscoroutinefunction

logger = logging.getLogger("perf")


def aelapsed(corofn, caption=""):
    async def wrapper(*args, **kwargs):
        t0 = perf_counter()
        result = await corofn(*args, **kwargs)
        delta = (perf_counter() - t0) * 1e3
        logger.info(f"{caption} Elapsed: {delta:.2f} ms")
        return result

    return wrapper


def aprofiler(cls, bases, members):
    for k, v in members.items():
        if iscoroutinefunction(v):
            members[k] = aelapsed(v, k)
    return type.__new__(type, cls, bases, members)
