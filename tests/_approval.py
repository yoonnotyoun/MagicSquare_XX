"""Approval test harness — golden baseline (.approved.txt) 비교."""

from __future__ import annotations

from pathlib import Path

_GOLDEN_DIR = Path(__file__).parent / "golden"


def approved_path(basename: str) -> Path:
    """`tests/golden/` 아래 approved 파일 경로."""
    if not basename.endswith(".approved.txt"):
        basename = f"{basename}.approved.txt"
    return _GOLDEN_DIR / basename


def verify_approved(actual: str, basename: str) -> None:
    """actual 문자열이 approved 기준 파일과 일치하는지 검증한다."""
    path = approved_path(basename)
    if not path.exists():
        raise FileNotFoundError(
            f"Approved baseline missing: {path}\n"
            f"--- actual (기준 파일 생성용) ---\n{actual}"
        )
    expected = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(
            f"Approval mismatch — {path.name}\n"
            f"--- expected ---\n{expected}"
            f"--- actual ---\n{actual}"
        )
