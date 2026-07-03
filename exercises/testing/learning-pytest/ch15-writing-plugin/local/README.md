# Local conftest Plugin

Skip slow tests:

```shell
pytest -v
```

Run all the tests, including slow:

```shell
pytest -v --slow
```

Run only slow tests:

```shell
pytest -v -m slow --slow
```
