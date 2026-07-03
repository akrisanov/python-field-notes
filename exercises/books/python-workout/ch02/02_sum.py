from collections.abc import Iterable, Sequence
from typing import Any

Number = int | float


def mysum(nums: Iterable[Number], start: float = 0.0) -> float:
    total = float(start)
    for num in nums:
        total += num
    return total


def sum_obj(objects: Iterable[Any], start: float = 0.0) -> float:
    total = float(start)

    for obj in objects:
        if isinstance(obj, bool):
            continue

        try:
            total += int(obj)
        except (TypeError, ValueError):
            pass

    return total


def avg(nums: Sequence[Number]) -> float:
    return mysum(nums) / len(nums)


def stats(words: list[str]) -> tuple[int, int, float]:
    if not words:
        return 0, 0, 0.0

    lengths = list(map(len, words))
    return min(lengths), max(lengths), avg(lengths)


if __name__ == "__main__":
    print(mysum([], 15))
    print(mysum([1, 2, 3], 10))
    print(mysum((15, 15, 24)))

    print(avg([10, 10, 10]))

    print(stats(["hello", "world", "me", "all", "Python"]))
    print(stats([]))

    print(sum_obj([]))
    print(sum_obj([1, "1", 0, "4", [1, 2, 3], 5], 10))
