# Python Field Notes

Personal learning notes, examples, and exercises for Python.

This repository combines:

- notebook-based study materials
- practical code snippets for standard library and third-party packages
- selected assignments from the Coursera course "Diving in Python"
- small experiments and utilities

## Quick Start

### 1. Install with uv

```shell
uv sync
```

This creates and manages a project environment from `pyproject.toml`.

Run tools with `uv run`:

```shell
uv run jupyter lab
# or
uv run jupyter notebook
```

### 2. Launch Jupyter

You can use either Jupyter Notebook or JupyterLab:

```shell
uv run jupyter notebook
# or
uv run jupyter lab
```

## Repository Structure

- `docs/`: repository navigation and learning-path docs
- `notes/tutorial/`: core Python notes from basics to advanced topics (functions, classes, generators, regex, testing, performance, serialization, concurrency)
- `notes/packages/`: package-focused examples (`numpy`, `matplotlib`, `sqlalchemy`, `logging`, `itertools`, and more)
- `notes/tips_and_tricks/`: concise practical examples and experiments
- `notes/frameworks/`: framework-related notes (for example, Django notebook)
- `exercises/coursera/`: solutions and materials from Coursera Python courses
- `exercises/books/python-workout/`: chapter-based Python Workout exercises
- `examples/async-and-io/learning-asyncio/`: async programming and networking examples
- `examples/assets/`: supporting scripts, fixtures, and tests for smaller exercises
- `examples/packagesample/`: a minimal Python package layout example
- `tooling/`: development environment notes (virtual environments, VS Code, docs)

## Using the Repository

### Learning path suggestion

1. Start with `notes/tutorial/00_intro.ipynb` and follow files in order.
2. Explore `notes/packages/` when you need targeted package examples.
3. Use `notes/tips_and_tricks/` for quick practical patterns.
4. Check `exercises/coursera/` for assignment-style practice.
5. Practice book-style tasks in `exercises/books/python-workout/`.
6. Explore async examples in `examples/async-and-io/learning-asyncio/`.

### Working in VS Code REPL

Open the command palette and run:

- `Python: Start REPL`

Then inspect built-in docs, for example:

```pycon
>>> help(str)
>>> help(str.upper)
```

If you use uv, you can also start IPython with:

```shell
uv run ipython
```

## References

### The history of Python

- [Guido van Rossum: The Early Years of Python](https://youtu.be/xLVxoz-mQFs)
- [Guido van Rossum: The Modern Era of Python](https://youtu.be/rTTFh7HOlC0)
- [Guido van Rossum: BDFL Python 3 retrospective](https://youtu.be/Oiw23yfqQy8)

### Selected PEPs

- [PEP 257 -- Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [PEP 440 -- Version Identification and Dependency Specification](https://www.python.org/dev/peps/pep-0440/)

## License

Copyright (C) 2019-2026 Andrey Krisanov.

Licensed under the MIT License. See `LICENSE` for details.
