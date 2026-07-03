# pytest

## Resources

* [Full pytest documentation](https://docs.pytest.org/en/latest/contents.html#)
* [pytest-cache documentation](http://pythonhosted.org/pytest-cache/)
* [Working with custom markers](https://docs.pytest.org/en/latest/example/markers.html)
* [pytest fixtures, parameterized fixtures](https://docs.pytest.org/en/latest/fixture.html)
* [pytest-xdist – Running Tests In Parallel](https://pypi.org/project/pytest-xdist/)

## Running Tests

| Command                                      | Description                                         |
| -------------------------------------------- | --------------------------------------------------- |
| pip3 install pytest pytest-cache pytest-pep8 | Install pytest                                      |
| python3 -m pytest --version                  | Run the Python 3 version of pytest                  |
| pytest -v hello_world_test.py                | Run all tests for hello_world.py (`-v` verbose mode)|
| pytest -x hello_world_test.py                | Stop after first failure                            |
| pytest --ff hello_world_test.py              | Run failed tests first                              |
| pytest -x --ff hello_world_test.py           | _Recommended approach_                              |
| pytest --pdb hello_world_test.py             | Drop you into the Python debugger when a test fails |
| pytest --pep8 hello_world_test.py            | Test for compliance to the style guide              |
| pytest -v tests/ -k test_view_status         | Run all tests matching the name                     |

## Skipping tests

```python
pytest.skip()
@pytest.mark.skip
@pytest.mark.skipif
```
