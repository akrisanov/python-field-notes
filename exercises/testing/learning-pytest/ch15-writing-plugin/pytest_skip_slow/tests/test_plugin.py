import pytest

# The pytester documentation lists a bunch of functions to help populate this directory:
# • makefile() creates a file of any kind.
# • makepyfile() creates a python file. This is commonly used to create test files.
# • makeconftest() creates conftest.py.
# • makeini() creates a tox.ini.
# • makepyprojecttoml() creates pyproject.toml.
# • maketxtfile() ... you get the picture.
# • mkdir() and mkpydir() create test subdirectories with or without __init__.py.
# • copy_example() copies files from the project’s directory to the temporary
#   directory. This is my favorite and what we’ll be using for testing our plugin.


@pytest.fixture()
def examples(pytester):
    pytester.copy_example("examples/test_slow.py")


def test_skip_slow(pytester, examples):
    result = pytester.runpytest("-v")
    # https://docs.python.org/3/library/fnmatch.html#fnmatch.fnmatch
    result.stdout.fnmatch_lines(
        [
            "*test_normal PASSED*",
            "*test_slow SKIPPED (need --slow option to run)*",
        ]
    )
    result.assert_outcomes(passed=1, skipped=1)


def test_run_slow(pytester, examples):
    result = pytester.runpytest("--slow")
    result.assert_outcomes(passed=2)


def test_run_only_slow(pytester, examples):
    result = pytester.runpytest("-v", "-m", "slow", "--slow")
    result.stdout.fnmatch_lines(["*test_slow PASSED*"])
    outcomes = result.parseoutcomes()
    assert outcomes["passed"] == 1
    assert outcomes["deselected"] == 1


def test_help(pytester):
    result = pytester.runpytest("--help")
    result.stdout.fnmatch_lines(["*--slow * include tests marked slow*"])
