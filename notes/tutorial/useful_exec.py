def boo():
    return 4

def test():
    assert boo() == 4

if __name__ == "__main__":
    print("Running tests...")
    test()
    print("OK")
