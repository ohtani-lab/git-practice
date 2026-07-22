#!/usr/bin/env python3
"""Small standard-library-only evaluation script for the Git practice."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate absolute errors in a sample measurement CSV."
    )
    parser.add_argument("--config", required=True, type=Path, help="JSON config path")
    parser.add_argument("--data", required=True, type=Path, help="CSV data path")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional Markdown report output path",
    )
    return parser.parse_args()


def load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("r", encoding="utf-8") as file:
        config = json.load(file)

    threshold = config.get("threshold")
    if not isinstance(threshold, (int, float)) or threshold < 0:
        raise ValueError("config.threshold must be a non-negative number")
    return config


def load_errors(path: Path) -> list[float]:
    if not path.is_file():
        raise FileNotFoundError(f"Data file not found: {path}")

    errors: list[float] = []
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        required = {"reference", "measurement"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(
                "CSV must contain 'reference' and 'measurement' columns"
            )
        for line_number, row in enumerate(reader, start=2):
            try:
                reference = float(row["reference"])
                measurement = float(row["measurement"])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid numeric value at CSV line {line_number}") from exc
            errors.append(round(abs(measurement - reference), 12))

    if not errors:
        raise ValueError("CSV contains no measurement rows")
    return errors


def calculate_metrics(errors: list[float], threshold: float) -> dict[str, float | int]:
    within = sum(error <= threshold for error in errors)
    return {
        "sample_count": len(errors),
        "mean_error": mean(errors),
        "max_error": max(errors),
        "threshold": threshold,
        "within_threshold_rate": within / len(errors),
    }


def format_report(
    config_path: Path,
    data_path: Path,
    config: dict[str, Any],
    metrics: dict[str, float | int],
) -> str:
    generated_at = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    experiment_name = str(config.get("experiment_name", "unnamed-experiment"))
    note = str(config.get("note", ""))

    return f"""# Experiment Report: {experiment_name}

## Metadata

- Generated at: {generated_at}
- Config: `{config_path.as_posix()}`
- Data: `{data_path.as_posix()}`
- Note: {note or '(none)'}

## Parameters

- threshold: {float(metrics['threshold']):.4f}

## Results

- sample_count: {int(metrics['sample_count'])}
- mean_error: {float(metrics['mean_error']):.4f}
- max_error: {float(metrics['max_error']):.4f}
- within_threshold_rate: {float(metrics['within_threshold_rate']):.4f}

## Discussion

Write what the result means and what should be tested next.
"""


def main() -> int:
    args = parse_args()
    try:
        config = load_config(args.config)
        errors = load_errors(args.data)
        metrics = calculate_metrics(errors, float(config["threshold"]))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}")
        return 1

    print(f"sample_count: {int(metrics['sample_count'])}")
    print(f"mean_error: {float(metrics['mean_error']):.4f}")
    print(f"max_error: {float(metrics['max_error']):.4f}")
    print(f"threshold: {float(metrics['threshold']):.4f}")
    print(f"within_threshold_rate: {float(metrics['within_threshold_rate']):.4f}")

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        report = format_report(args.config, args.data, config, metrics)
        args.output.write_text(report, encoding="utf-8")
        print(f"report_written: {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
