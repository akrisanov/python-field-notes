# pytest_skip_slow

A pytest plugin to skip `@pytest.mark.slow` tests by default.
Include the slow tests with `--slow`.

## Building the package

```shell
flit build
```

## Installing the package

```shell
pip install dist/pytest_skip_slow-0.0.1-py3-none-any.whl
```

## Running tests

```shell
pytest examples/test_slow.py
```

```shell
pytest --slow examples/test_slow.py
```

## Publishing the plugin

To publish your plugin, you can:

1. Push your plugin code to a Git repository and install from there.
    - For example: pip install git+https://github.com/okken/pytest-skip-slow
    - Note that you can list multiple git+https://... repositories in a requirements.txt file
      and as dependencies in tox.ini.

2. Copy the wheel, pytest_skip_slow-0.0.1-py3-none-any.whl, to a shared directory somewhere and install from there.
    – cp dist/*.whl path/to/my_packages/
    – pip install pytest-skip-slow --no-index --find-links=path/to/my_packages/

3. Publish to PyPI.
    - Check out the [Uploading the distribution archives section](https://packaging.python.org/tutorials/packaging-projects/#uploading-the-distribution-archives) in Python's documentation on packaging.
    - Also see the [Controlling package uploads](https://flit.readthedocs.io/en/latest/upload.html#controlling-package-uploads) section of the Flit documentation.
