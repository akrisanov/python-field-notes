

# Notas de Campo de Python

Notas de aprendizaje personal, ejemplos y ejercicios para Python.

Este repositorio combina:

- materiales de estudio basados en notebooks
- fragmentos de código prácticos para la biblioteca estándar y paquetes de terceros
- asignaturas seleccionadas del curso de Coursera "Diving in Python"
- pequeños experimentos y utilidades

## Inicio Rápido

### 1. Instalar con uv

```shell
uv sync
```

Esto crea y administra un entorno de proyecto desde `pyproject.toml`.

Ejecuta herramientas con `uv run`:

```shell
uv run jupyter lab
# o
uv run jupyter notebook
```

### 2. Iniciar Jupyter

Puedes usar Jupyter Notebook o JupyterLab:

```shell
uv run jupyter notebook
# o
uv run jupyter lab
```

## Estructura del Repositorio

- `docs/`: documentación de navegación del repositorio y rutas de aprendizaje
- `notes/tutorial/`: notas centrales de Python desde lo básico hasta temas avanzados (funciones, clases, generadores, expresiones regulares, pruebas, rendimiento, serialización, concurrencia)
- `notes/packages/`: ejemplos centrados en paquetes (`numpy`, `matplotlib`, `sqlalchemy`, `logging`, `itertools`, y más)
- `notes/tips_and_tricks/`: ejemplos prácticos concisos y experimentos
- `notes/frameworks/`: notas relacionadas con frameworks (por ejemplo, notebook de Django)
- `exercises/coursera/`: soluciones y materiales de los cursos de Python de Coursera
- `exercises/books/python-workout/`: ejercicios de Python Workout organizados por capítulos
- `exercises/testing/learning-pytest/`: proyecto de aprendizaje de pytest organizado por capítulos
- `examples/async-and-io/learning-asyncio/`: ejemplos de programación asíncrona y redes
- `examples/databases/learning-sqlalchemy/`: ejemplos de consultas y ORM con SQLAlchemy
- `examples/assets/`: scripts de apoyo, fixtures y pruebas para ejercicios menores
- `examples/packagesample/`: ejemplo de estructura mínima de un paquete de Python
- `tooling/`: notas del entorno de desarrollo (entornos virtuales, VS Code, documentación)

## Uso del Repositorio

### Sugerencia de ruta de aprendizaje

1. Comienza con `notes/tutorial/00_intro.ipynb` y sigue los archivos en orden.
2. Explora `notes/packages/` cuando necesites ejemplos específicos de paquetes.
3. Usa `notes/tips_and_tricks/` para patrones prácticos rápidos.
4. Consulta `exercises/coursera/` para práctica tipo asignatura.
5. Practica tareas tipo libro en `exercises/books/python-workout/`.
6. Practica tareas enfocadas en pruebas en `exercises/testing/learning-pytest/`.
7. Explora ejemplos asíncronos en `examples/async-and-io/learning-asyncio/`.
8. Explora ejemplos de SQLAlchemy en `examples/databases/learning-sqlalchemy/`.

### Trabajar en el REPL de VS Code

Abre la paleta de comandos y ejecuta:

- `Python: Start REPL`

Luego inspecciona la documentación incorporada, por ejemplo:

```pycon
>>> help(str)
>>> help(str.upper)
```

Si usas uv, también puedes iniciar IPython con:

```shell
uv run ipython
```

## Referencias

### La historia de Python

- [Guido van Rossum: The Early Years of Python](https://youtu.be/xLVxoz-mQFs)
- [Guido van Rossum: The Modern Era of Python](https://youtu.be/rTTFh7HOlC0)
- [Guido van Rossum: BDFL Python 3 retrospective](https://youtu.be/Oiw23yfqQy8)

### PEPs seleccionados

- [PEP 257 -- Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [PEP 440 -- Version Identification and Dependency Specification](https://www.python.org/dev/peps/pep-0440/)

## Licencia

Copyright (C) 2019-2026 Andrey Krisanov.

Licenciado bajo la Licencia MIT. Consulta `LICENSE` para más detalles.
