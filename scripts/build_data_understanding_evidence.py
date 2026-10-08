import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "src"))

from warehouse_operations_analytics.data_understanding import main

if __name__ == "__main__":
    raise SystemExit(main())
