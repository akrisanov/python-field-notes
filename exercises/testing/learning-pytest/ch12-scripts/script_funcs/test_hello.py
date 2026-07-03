import hello


def test_full_output():
    assert hello.full_output() == "Hello, World!"


def test_main(capsys):
    hello.main()
    output = capsys.readouterr().out
    assert output == "Hello, World!\n"
