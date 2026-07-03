# pytest -s tests/test_sys_path.py
import sys


def test_sys_path():
    print("sys.path: ")
    for p in sys.path:
        print(p)
