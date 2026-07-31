from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def test_required_project_files_exist() -> None:
    required_paths = [
        "README.md",
        "PROJECT_CHARTER.md",
        "data/README.md",
        "requirements.txt",
        "notebooks",
        "reports/figures",
        "sql",
        "src/warehouse_operations_analytics",
    ]

    missing = [
        path
        for path in required_paths
        if not (REPOSITORY_ROOT / path).exists()
    ]

    assert not missing, f"Missing required project paths: {missing}"
