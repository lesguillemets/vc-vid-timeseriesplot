# Coding Guidelines for AI Agents

This document provides instructions for AI coding agents working on the vptry-facelandmarkview codebase.


## General

- Target python 3.14, which means you may use newer syntaxes and functionalities provided by python.
- Always prefer polars and avoid pandas.
- Split functions, so that each function has its clear meaning and granular function. Unless it makes the code clearer, avoid one large function that does everything.
- Prefer British spelling.

## Commits

- Make granular commits, so that the intent and the content of each commit is clear.

## Comments

- Make enough comment to make the code readable, and friendly for other developpers,
  but refrain from making too obvious comments.

## Code Formatting

- Always format code using ruff before committing for files you edit.

```bash
# Format specific files
uv run ruff format path/to/file.py
```

- Verify formatting is applied before committing

## Code Linting

- Always lint and fix code using Ruff before committing for files you edit.

```bash
# Lint specific files
ruff check --fix path/to/file.py
```

- All Python code you edit must pass Ruff linting
- Run `ruff check --fix path/to/file.py` to automatically fix issues
- Address any remaining lint warnings/errors manually
- Verify all lint issues are resolved before committing

## Type Annotations

All Python code must be well type-annotated.

### Type Annotation Best Practices

- Use `typing` module types: `Optional`, `Union`, `Callable`, etc.
- Use `numpy.typing` for NumPy arrays: `npt.NDArray[np.float64]`
- Use modern type syntax where supported (Python 3.12+):
  - `list[int]` instead of `List[int]`
  - `dict[str, int]` instead of `Dict[str, int]`
  - `set[int]` instead of `Set[int]`
  - `tuple[int, str]` instead of `Tuple[int, str]`
- Use `| None` syntax instead of `Optional` for Python 3.10+
- Use specific collection types over generic ones

### Type Checking

Run `uv run pyright` to check for type issues.
Address type errors when practical. If the fix for typing introduces a lot of change, leave it as it is, and have a human handel it.

## Path Handling

**Prefer `pathlib.Path` over string paths.**

### Do This ✓

```python
from pathlib import Path

def load_file(filepath: Path) -> None:
    """Load data from file."""
    if filepath.exists():
        data = filepath.read_text()
    parent_dir = filepath.parent
    filename = filepath.name
```

```python
# When receiving paths from user input or arguments
import argparse
parser.add_argument("file", type=Path, help="Path to file")
```

```python
# Building paths
config_dir = Path("~/.config/myapp").expanduser()
data_file = config_dir / "data.json"
```

### Path Type Annotations

- Function parameters accepting paths: use `Path`
- When paths can be strings or Path objects: use `Path | str` or `Union[Path, str]`
- Convert string inputs to Path early: `path = Path(path_input)`

## Matplotlib

If you use Matplotlib,

- Always prefer object-oriented syntax, rather than pyplot syntax.
- Refrain from using function like `plt.plot` etc., and explicitly call methods or functions for Axes, Axis, Figure, etc.

## Readme

- Write readme for other developers, and not users.
- Don't praise anything about the project; keep the tone direct and professional.
- Never ever use emojis.
- Prefer British spelling.


## Additional Notes

- The codebase follows a modular src-layout structure
- Maintain consistency with existing code style and patterns
- Keep changes minimal and focused
- Document complex logic with clear comments when necessary
