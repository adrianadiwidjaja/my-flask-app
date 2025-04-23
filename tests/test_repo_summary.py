from pathlib import Path
from tools.repo_summary import generate_summary


def test_summary_counts():
    project_root = Path(__file__).resolve().parents[1]
    summary = generate_summary(project_root)

    assert summary['python_files'] >= 1
    assert summary['tests'] >= 1
    assert summary['models'] >= 1

    # Check that keys exist
    assert set(summary.keys()) == {'python_files', 'tests', 'models'}
