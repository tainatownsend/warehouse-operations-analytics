"""Build reproducible, claim-safe evidence from the local raw CSV snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
import numbers
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd

COLUMN_PROFILE_COLUMNS = [
    "table",
    "column",
    "dtype",
    "row_count",
    "non_null_count",
    "null_count",
    "null_rate",
    "unique_count",
    "is_unique_when_present",
]

TEMPORAL_PROFILE_COLUMNS = [
    "table",
    "column",
    "row_count",
    "source_non_null_count",
    "parsed_count",
    "invalid_count",
    "missing_count",
    "minimum_utc",
    "maximum_utc",
]

RELATIONSHIP_COLUMNS = [
    "name",
    "status",
    "child",
    "parent",
    "child_non_null_count",
    "parent_non_null_count",
    "orphan_count",
    "parent_duplicate_count",
    "child_duplicate_count",
    "observed_cardinality",
    "reason",
]


class EvidenceBoundaryError(RuntimeError):
    """Raised when the configured evidence boundary cannot be satisfied."""


@dataclass(frozen=True)
class EvidencePaths:
    inventory: Path
    columns: Path
    temporal: Path
    relationships: Path
    report: Path


def load_config(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as config_file:
        config = json.load(config_file)

    required = {"expected_tables", "temporal_fields", "relationships"}
    missing = required.difference(config)
    if missing:
        raise EvidenceBoundaryError(
            f"Configuration is missing required keys: {sorted(missing)}"
        )
    return config


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def discover_csvs(raw_dir: Path) -> dict[str, Path]:
    return {
        path.stem: path
        for path in sorted(raw_dir.glob("*.csv"))
        if path.is_file()
    }


def validate_snapshot(
    csv_files: dict[str, Path],
    expected_tables: list[str],
    allow_partial: bool,
) -> tuple[list[str], list[str]]:
    found = set(csv_files)
    expected = set(expected_tables)
    missing = sorted(expected - found)
    unexpected = sorted(found - expected)

    if not csv_files:
        raise EvidenceBoundaryError(
            "No CSV files were found. Restore the raw snapshot under data/raw/."
        )
    if missing and not allow_partial:
        raise EvidenceBoundaryError(
            "Raw snapshot is incomplete. Missing tables: " + ", ".join(missing)
        )
    return missing, unexpected


def read_tables(csv_files: dict[str, Path]) -> dict[str, pd.DataFrame]:
    return {
        table: pd.read_csv(path, low_memory=False)
        for table, path in csv_files.items()
    }


def build_inventory(
    csv_files: dict[str, Path],
    tables: dict[str, pd.DataFrame],
) -> list[dict[str, Any]]:
    return [
        {
            "table": table,
            "file_name": csv_files[table].name,
            "size_bytes": csv_files[table].stat().st_size,
            "sha256": sha256_file(csv_files[table]),
            "row_count": len(frame),
            "column_count": len(frame.columns),
        }
        for table, frame in sorted(tables.items())
    ]


def build_column_profile(
    tables: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for table, frame in sorted(tables.items()):
        for column in frame.columns:
            series = frame[column]
            non_null_count = int(series.notna().sum())
            unique_count = int(series.nunique(dropna=True))
            rows.append(
                {
                    "table": table,
                    "column": column,
                    "dtype": str(series.dtype),
                    "row_count": len(series),
                    "non_null_count": non_null_count,
                    "null_count": int(series.isna().sum()),
                    "null_rate": round(float(series.isna().mean()), 6),
                    "unique_count": unique_count,
                    "is_unique_when_present": (
                        non_null_count > 0 and unique_count == non_null_count
                    ),
                }
            )
    return pd.DataFrame(rows, columns=COLUMN_PROFILE_COLUMNS)


def build_temporal_profile(
    tables: dict[str, pd.DataFrame],
    temporal_fields: list[str],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for table, frame in sorted(tables.items()):
        for column in temporal_fields:
            if column not in frame.columns:
                continue

            source = frame[column]
            parsed = pd.to_datetime(source, errors="coerce", utc=True)
            source_non_null = int(source.notna().sum())
            parsed_non_null = int(parsed.notna().sum())
            minimum = parsed.min()
            maximum = parsed.max()
            rows.append(
                {
                    "table": table,
                    "column": column,
                    "row_count": len(source),
                    "source_non_null_count": source_non_null,
                    "parsed_count": parsed_non_null,
                    "invalid_count": source_non_null - parsed_non_null,
                    "missing_count": int(source.isna().sum()),
                    "minimum_utc": (
                        minimum.isoformat() if pd.notna(minimum) else None
                    ),
                    "maximum_utc": (
                        maximum.isoformat() if pd.notna(maximum) else None
                    ),
                }
            )
    return pd.DataFrame(rows, columns=TEMPORAL_PROFILE_COLUMNS)


def _normalized_keys(series: pd.Series) -> pd.Series:
    def normalize(value: Any) -> str:
        if isinstance(value, numbers.Integral):
            return str(int(value))
        if isinstance(value, numbers.Real) and float(value).is_integer():
            return str(int(value))
        return str(value).strip()

    return series.dropna().map(normalize).astype("string")


def build_relationship_profile(
    tables: dict[str, pd.DataFrame],
    relationships: list[dict[str, str]],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for relationship in relationships:
        name = relationship["name"]
        child_table = relationship["child_table"]
        child_column = relationship["child_column"]
        parent_table = relationship["parent_table"]
        parent_column = relationship["parent_column"]

        missing_references = [
            reference
            for reference, exists in (
                (child_table, child_table in tables),
                (parent_table, parent_table in tables),
                (
                    f"{child_table}.{child_column}",
                    child_table in tables
                    and child_column in tables[child_table].columns,
                ),
                (
                    f"{parent_table}.{parent_column}",
                    parent_table in tables
                    and parent_column in tables[parent_table].columns,
                ),
            )
            if not exists
        ]
        if missing_references:
            rows.append(
                {
                    "name": name,
                    "status": "not_tested",
                    "child": f"{child_table}.{child_column}",
                    "parent": f"{parent_table}.{parent_column}",
                    "reason": "Missing: " + ", ".join(missing_references),
                }
            )
            continue

        child_keys = _normalized_keys(tables[child_table][child_column])
        parent_keys = _normalized_keys(tables[parent_table][parent_column])
        parent_key_set = set(parent_keys)
        orphan_count = int((~child_keys.isin(parent_key_set)).sum())
        parent_duplicates = int(parent_keys.duplicated().sum())
        child_duplicates = int(child_keys.duplicated().sum())

        if parent_duplicates:
            observed_cardinality = "invalid_parent_key"
        elif child_duplicates:
            observed_cardinality = "many_to_one"
        else:
            observed_cardinality = "one_to_one_in_snapshot"

        rows.append(
            {
                "name": name,
                "status": "tested",
                "child": f"{child_table}.{child_column}",
                "parent": f"{parent_table}.{parent_column}",
                "child_non_null_count": len(child_keys),
                "parent_non_null_count": len(parent_keys),
                "orphan_count": orphan_count,
                "parent_duplicate_count": parent_duplicates,
                "child_duplicate_count": child_duplicates,
                "observed_cardinality": observed_cardinality,
                "reason": "",
            }
        )
    return pd.DataFrame(rows, columns=RELATIONSHIP_COLUMNS)


def evidence_paths(output_dir: Path, report_path: Path) -> EvidencePaths:
    return EvidencePaths(
        inventory=output_dir / "data_inventory.json",
        columns=output_dir / "column_profile.csv",
        temporal=output_dir / "temporal_profile.csv",
        relationships=output_dir / "relationship_profile.csv",
        report=report_path,
    )


def write_outputs(
    paths: EvidencePaths,
    inventory: list[dict[str, Any]],
    columns: pd.DataFrame,
    temporal: pd.DataFrame,
    relationships: pd.DataFrame,
    missing_tables: list[str],
    unexpected_tables: list[str],
) -> None:
    paths.inventory.parent.mkdir(parents=True, exist_ok=True)
    paths.report.parent.mkdir(parents=True, exist_ok=True)

    paths.inventory.write_text(
        json.dumps(inventory, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    columns.to_csv(paths.columns, index=False)
    temporal.to_csv(paths.temporal, index=False)
    relationships.to_csv(paths.relationships, index=False)

    total_rows = sum(item["row_count"] for item in inventory)
    relationship_summary = (
        "No relationships were configured; no referential-integrity or "
        "cardinality conclusion is available."
        if relationships.empty
        else f"{len(relationships)} configured relationships were evaluated."
    )
    report = [
        "# Data Understanding Evidence",
        "",
        f"Generated at: {datetime.now(UTC).isoformat()}",
        "",
        "## Snapshot",
        "",
        f"- Tables profiled: {len(inventory)}",
        f"- Rows profiled: {total_rows}",
        f"- Missing expected tables: {', '.join(missing_tables) or 'None'}",
        f"- Unexpected tables: {', '.join(unexpected_tables) or 'None'}",
        "",
        "## Evidence Files",
        "",
        f"- `{paths.inventory.name}`: file identity, checksums, rows and columns",
        f"- `{paths.columns.name}`: nulls, dtypes and uniqueness candidates",
        f"- `{paths.temporal.name}`: parsing, coverage and invalid values",
        f"- `{paths.relationships.name}`: configured FK/cardinality tests",
        "",
        "## Relationship Boundary",
        "",
        relationship_summary,
        "",
        "## Interpretation Rule",
        "",
        (
            "These outputs are observations from one preserved snapshot. Key "
            "names, business semantics and authoritative time grain require "
            "documented interpretation before they become analytical conclusions."
        ),
        "",
    ]
    paths.report.write_text("\n".join(report), encoding="utf-8")


def run_evidence_build(
    raw_dir: Path,
    output_dir: Path,
    report_path: Path,
    config_path: Path,
    allow_partial: bool = False,
) -> EvidencePaths:
    config = load_config(config_path)
    csv_files = discover_csvs(raw_dir)
    missing, unexpected = validate_snapshot(
        csv_files,
        config["expected_tables"],
        allow_partial,
    )
    tables = read_tables(csv_files)
    inventory = build_inventory(csv_files, tables)
    columns = build_column_profile(tables)
    temporal = build_temporal_profile(tables, config["temporal_fields"])
    relationships = build_relationship_profile(tables, config["relationships"])
    paths = evidence_paths(output_dir, report_path)
    write_outputs(
        paths,
        inventory,
        columns,
        temporal,
        relationships,
        missing,
        unexpected,
    )
    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build reproducible data-understanding evidence from raw CSVs."
    )
    parser.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    parser.add_argument(
        "--output-dir", type=Path, default=Path("data/processed")
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("reports/data_understanding_evidence.md"),
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/data_understanding.json"),
    )
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="Profile a partial snapshot without treating missing tables as fatal.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        paths = run_evidence_build(
            raw_dir=args.raw_dir,
            output_dir=args.output_dir,
            report_path=args.report,
            config_path=args.config,
            allow_partial=args.allow_partial,
        )
    except EvidenceBoundaryError as error:
        print(f"Evidence build blocked: {error}")
        return 2

    print(f"Evidence build completed: {paths.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
