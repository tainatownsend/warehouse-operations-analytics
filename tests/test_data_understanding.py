import json
from pathlib import Path

import pandas as pd
import pytest

from warehouse_operations_analytics.data_understanding import (
    EvidenceBoundaryError,
    run_evidence_build,
)


def write_config(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "expected_tables": ["loads", "routes"],
                "temporal_fields": ["load_date"],
                "relationships": [
                    {
                        "name": "loads_to_routes",
                        "child_table": "loads",
                        "child_column": "route_id",
                        "parent_table": "routes",
                        "parent_column": "route_id",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )


def test_builds_reproducible_snapshot_evidence(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    output_dir = tmp_path / "processed"
    report_path = tmp_path / "reports" / "evidence.md"
    config_path = tmp_path / "config.json"
    raw_dir.mkdir()
    write_config(config_path)

    pd.DataFrame(
        {
            "route_id": [10, 20],
            "origin": ["A", "B"],
        }
    ).to_csv(raw_dir / "routes.csv", index=False)
    pd.DataFrame(
        {
            "load_id": [1, 2, 3],
            "route_id": [10, 10, 99],
            "load_date": ["2026-01-01", "bad-date", None],
        }
    ).to_csv(raw_dir / "loads.csv", index=False)

    paths = run_evidence_build(
        raw_dir,
        output_dir,
        report_path,
        config_path,
    )

    inventory = json.loads(paths.inventory.read_text(encoding="utf-8"))
    assert [item["table"] for item in inventory] == ["loads", "routes"]
    assert all(len(item["sha256"]) == 64 for item in inventory)

    temporal = pd.read_csv(paths.temporal)
    assert temporal.loc[0, "parsed_count"] == 1
    assert temporal.loc[0, "invalid_count"] == 1
    assert temporal.loc[0, "missing_count"] == 1

    relationships = pd.read_csv(paths.relationships)
    assert relationships.loc[0, "orphan_count"] == 1
    assert relationships.loc[0, "observed_cardinality"] == "many_to_one"
    assert "observations from one preserved snapshot" in paths.report.read_text(
        encoding="utf-8"
    )


def test_rejects_an_incomplete_snapshot_by_default(tmp_path: Path) -> None:
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    pd.DataFrame({"load_id": [1]}).to_csv(
        raw_dir / "loads.csv", index=False
    )
    config_path = tmp_path / "config.json"
    write_config(config_path)

    with pytest.raises(EvidenceBoundaryError, match="Missing tables: routes"):
        run_evidence_build(
            raw_dir,
            tmp_path / "processed",
            tmp_path / "report.md",
            config_path,
        )


def test_allows_partial_profile_without_claiming_relationships(
    tmp_path: Path,
) -> None:
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    pd.DataFrame({"load_id": [1]}).to_csv(
        raw_dir / "loads.csv", index=False
    )
    config_path = tmp_path / "config.json"
    write_config(config_path)

    paths = run_evidence_build(
        raw_dir,
        tmp_path / "processed",
        tmp_path / "report.md",
        config_path,
        allow_partial=True,
    )

    relationships = pd.read_csv(paths.relationships)
    assert relationships.loc[0, "status"] == "not_tested"
    assert "Missing: routes" in relationships.loc[0, "reason"]
