from threading import Thread


class HelloThread(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        print("Hello,", self.name)


p = HelloThread("Andrey")
p.start()
p.join()
