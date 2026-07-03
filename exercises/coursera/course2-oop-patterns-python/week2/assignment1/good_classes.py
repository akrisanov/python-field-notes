from abc import ABC, abstractmethod
import math


class Base(ABC):
    def __init__(self, data, result):
        self.data = data
        self.result = result
        self.xy_pairs = zip(self.data, self.result)

    def get_answer(self):
        return [int(x >= 0.5) for x in self.data]

    def get_score(self):
        ans = self.get_answer()
        return sum([int(x == y) for x, y in zip(ans, self.result)]) / len(ans)

    @abstractmethod
    def get_loss(self):
        pass


class A(Base):
    def get_loss(self):
        return sum([(x - y) * (x - y) for x, y in self.xy_pairs])


class B(A):
    def get_res(self, answer):
        return [int(x == 1 and y == 1) for x, y in zip(answer, self.result)]

    def get_loss(self):
        return -sum([
            y * math.log(x) + (1 - y) * math.log(1 - x)
            for x, y in self.xy_pairs
        ])

    def get_pre(self):
        ans = self.get_answer()
        res = self.get_res(ans)
        return sum(res) / sum(ans)

    def get_rec(self):
        ans = self.get_answer()
        res = self.get_res(ans)
        return sum(res) / sum(self.result)

    def get_score(self):
        pre = self.get_pre()
        rec = self.get_rec()
        return 2 * pre * rec / (pre + rec)


class C(A):
    def get_loss(self):
        return sum([abs(x - y) for x, y in self.xy_pairs])
