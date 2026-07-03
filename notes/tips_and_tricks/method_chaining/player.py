import numpy as np


class Player:
    """Implement method chaining by returning an instance from each of its methods."""

    def __init__(self, name, position, fatigue=0) -> None:
        self.name = name
        self.position = position
        self.fatigue = fatigue

    def draw(self):
        print(f"drawing {self.name} to screen at {self.position}")
        return self

    def move(self, delta):
        self.position += delta
        self.fatigue += 1
        return self

    def rest(self):
        self.fatigue = 0
        return self


def main():
    andrey = Player("Andrey", np.array([0.0, 0.0]))
    up = np.array([0.0, 1.0])
    right = np.array([1.0, 0.0])

    # instead of writing this
    # andrey.move(up)
    # andrey.move(right)
    # andrey.move(up)
    # andrey.rest()
    # andrey.draw()

    # we do method chaining
    andrey.move(up).move(right).move(up).rest().draw()


if __name__ == "__main__":
    main()
