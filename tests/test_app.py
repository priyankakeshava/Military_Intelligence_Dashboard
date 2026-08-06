from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_resolve_data_path_uses_project_root():
    import app

    data_path = app.resolve_data_path()

    assert data_path == ROOT / "data" / "globalterrorism.csv"
    assert data_path.exists()
