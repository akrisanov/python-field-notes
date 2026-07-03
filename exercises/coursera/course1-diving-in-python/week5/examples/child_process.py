import time
import os

pid = os.fork()
if pid == 0:
    while True:
        print("child process:", os.getpid())
        time.sleep(5)
else:
    print("parent process:", os.getpid())
    os.wait()
