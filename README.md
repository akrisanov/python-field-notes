# Python Field Notes

Personal learning notes, examples, and exercises for Python.

This repository combines:

- notebook-based study materials
- practical code snippets for standard library and third-party packages
- selected assignments from the Coursera course "Diving in Python"
- small experiments and utilities

## Quick Start

### 1. Create and activate a virtual environment

```shell
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```shell
pip install -r requirements.txt
```

### 3. Launch Jupyter

You can use either Jupyter Notebook or JupyterLab:

```shell
jupyter notebook
# or
jupyter lab
```

## Repository Structure

- `assets/`: supporting scripts, fixtures, and tests for smaller exercises
- `coursera/`: solutions and materials from Coursera Python courses
- `frameworks/`: framework-related notes (for example, Django notebook)
- `packages/`: package-focused examples (`numpy`, `matplotlib`, `sqlalchemy`, `logging`, `itertools`, and more)
- `packagesample/`: a minimal Python package layout example.
- `tips_and_tricks/`: concise practical examples and experiments
- `tooling/`: development environment notes (virtual environments, VS Code, docs)
- `tutorial/`: core Python notes from basics to advanced topics (functions, classes, generators, regex, testing, performance, serialization, concurrency)

## Using the Repository

### Learning path suggestion

1. Start with `tutorial/00_intro.ipynb` and follow files in order.
2. Explore `packages/` when you need targeted package examples.
3. Use `tips_and_tricks/` for quick practical patterns.
4. Check `coursera/` for assignment-style practice.

### Working in VS Code REPL

Open the command palette and run:

- `Python: Start REPL`

Then inspect built-in docs, for example:

```pycon
>>> help(str)
>>> help(str.upper)
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
