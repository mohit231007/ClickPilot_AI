"""Schema and data-quality checks used by both UI and API."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from clickpilot.features import RAW_REQUIRED_COLUMNS


@dataclass
class AuditReport:
    status: str
    rows: int
    missing_by_column: dict[str, int]
    invalid_datetime_count: int
    duplicate_session_count: int
    missing_required_columns: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "rows": self.rows,
            "missing_by_column": self.missing_by_column,
            "invalid_datetime_count": self.invalid_datetime_count,
            "duplicate_session_count": self.duplicate_session_count,
            "missing_required_columns": self.missing_required_columns,
        }


def audit_impression_data(frame: pd.DataFrame) -> AuditReport:
    missing_required = [c for c in RAW_REQUIRED_COLUMNS if c not in frame.columns]
    missing_by_column = {
        c: int(frame[c].isna().sum()) for c in frame.columns if int(frame[c].isna().sum()) > 0
    }
    invalid_datetime = 0
    if "DateTime" in frame.columns:
        invalid_datetime = int(pd.to_datetime(frame["DateTime"], errors="coerce").isna().sum())
    duplicate_session = 0
    if "session_id" in frame.columns:
        duplicate_session = int(frame["session_id"].duplicated().sum())

    if missing_required or invalid_datetime:
        status = "requires_review"
    elif missing_by_column:
        status = "valid_with_missing_categories"
    else:
        status = "valid"

    return AuditReport(
        status=status,
        rows=len(frame),
        missing_by_column=missing_by_column,
        invalid_datetime_count=invalid_datetime,
        duplicate_session_count=duplicate_session,
        missing_required_columns=missing_required,
    )
