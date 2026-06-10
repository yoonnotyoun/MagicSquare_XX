"""T-GM-01 — golden master approval (FR-06 · SC-01·02 · control)."""

from _approval import verify_approved
from src.entity.constants import LINE_IDS
from src.entity.lines import sum_line
from src.validate_lines import validate_lines


def _format_validate_report(grid: list[list[int]], result: dict) -> str:
    """10선 합·validate_lines 결과를 approval 기준 텍스트로 직렬화."""
    lines = [
        "# T-GM-01 golden master",
        "grid:",
        *[(" ".join(f"{v:2d}" for v in row)) for row in grid],
        "line_sums:",
    ]
    for line_id in LINE_IDS:
        lines.append(f"  {line_id}={sum_line(line_id, grid)}")
    lines.append(f"status: {result['status']}")
    if result["failed_lines"]:
        lines.append("failed_lines: " + ", ".join(result["failed_lines"]))
    else:
        lines.append("failed_lines:")
    return "\n".join(lines) + "\n"


def test_gm_01_validate_pass_approval(grid_golden_pass):
    """Golden master — validate_lines pass 회귀 기준선 (approval)."""
    result = validate_lines(grid_golden_pass)
    actual = _format_validate_report(grid_golden_pass, result)
    verify_approved(actual, "gm_01_g1_validate_pass.approved.txt")
