import os
import ast
from collections import Counter
from pathlib import Path


def count_python_files(base_path: Path) -> int:
    """Return the number of Python files under ``base_path``.

    Parameters
    ----------
    base_path: Path
        Directory to search for ``.py`` files.
    """
    return sum(1 for _ in base_path.rglob('*.py'))


def count_models(models_path: Path) -> int:
    """Count SQLAlchemy model classes in ``models_path``.

    Only classes inheriting from ``db.Model`` are counted.
    """
    with models_path.open('r', encoding='utf-8') as f:
        tree = ast.parse(f.read(), filename=str(models_path))

    model_count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if (isinstance(base, ast.Attribute)
                        and base.attr == 'Model') or (
                    isinstance(base, ast.Name) and base.id == 'db.Model'):
                    model_count += 1
                    break
    return model_count


def count_tests(tests_path: Path) -> int:
    """Return the number of pytest files in ``tests_path``."""
    return sum(1 for _ in tests_path.glob('test_*.py'))


def generate_summary(project_root: Path) -> dict:
    """Generate a small summary of key repository statistics.

    Parameters
    ----------
    project_root: Path
        Location of the repository root.

    Returns
    -------
    dict
        Dictionary containing counts of interest. Keys are ``python_files``,
        ``tests`` and ``models``.
    """
    app_path = project_root / 'app'
    tests_path = project_root / 'tests'
    models_path = app_path / 'models.py'

    summary = {
        'python_files': count_python_files(project_root),
        'tests': count_tests(tests_path) if tests_path.exists() else 0,
        'models': count_models(models_path) if models_path.exists() else 0,
    }
    return summary


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    summary = generate_summary(root)
    print('Repository summary:')
    for key, value in summary.items():
        print(f'{key}: {value}')


if __name__ == '__main__':
    main()
