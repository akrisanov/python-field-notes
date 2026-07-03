from multiprocessing import Process


def hello(name):
    print("Hello,", name)


p = Process(target=hello, args=("Andrey",))
p.start()  # fork
p.join()   # wait for child processes
