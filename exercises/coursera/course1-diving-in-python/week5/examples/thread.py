from threading import Thread


def hello(name):
    print("Hello,", name)


t = Thread(target=hello, args=("Andrey",))
t.start()
t.join()
