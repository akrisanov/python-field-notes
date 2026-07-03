import numpy as np
from dataclasses import dataclass


@dataclass(frozen=True)
class Vector:
    x: float
    y: float
    z: float

    def normalized(self):
        x, y, z = self.x, self.y, self.z
        norm = np.sqrt(x * x + y * y + z * z)
        return type(self)(x / norm, y / norm, z / norm)

    def reflected(self):
        return type(self)(-self.x, -self.y, -self.z)


def main():
    p = Vector(1.0, 2.0, 3.0)
    q = p.reflected().normalized()
    print(p)
    print(q)


if __name__ == "__main__":
    main()
