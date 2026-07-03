import os

number = 42

if os.fork() == 0:
    number = 0
    print("child process:", number)
else:
    print("parent process:", number)
    os.wait()
