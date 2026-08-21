from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def test_required_project_files_exist() -> None:
    required_paths = [
        "README.md",
        "PROJECT_CHARTER.md",
        "config/data_understanding.json",
        "data/README.md",
        "requirements.txt",
        "notebooks",
        "reports/figures",
        "scripts/build_data_understanding_evidence.py",
        "sql",
        "src/warehouse_operations_analytics",
        "src/warehouse_operations_analytics/data_understanding.py",
    ]

    missing = [
        path
        for path in required_paths
        if not (REPOSITORY_ROOT / path).exists()
    ]

    assert not missing, f"Missing required project paths: {missing}"
