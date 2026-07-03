from hello_world import hello


def test_hello_v1():
    hello()
    output = open("hello.txt").read().rstrip()
    assert output == "Hello World!"


def test_hello_v2(monkeypatch, tmp_path_factory, capsys):
    output_dir = tmp_path_factory.mktemp("data")
    monkeypatch.chdir(output_dir)

    hello()

    output_path = output_dir / "hello.txt"

    with capsys.disabled():
        print("\nThe output path is", output_path)

    output = open(output_path).read().rstrip()
    assert output == "Hello World!"
