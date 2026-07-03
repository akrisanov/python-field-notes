from multiprocessing import Process


class HelloProcess(Process):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print("Hello,", self.name)


p = HelloProcess("Andrey")
p.start()
p.join()
