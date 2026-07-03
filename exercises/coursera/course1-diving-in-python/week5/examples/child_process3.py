import os

f = open("data.txt")
l = f.readline()

if os.fork() == 0:
    l = f.readline()
    print("child process:", l)
else:
    l = f.readline()
    print("parent process:", l)
