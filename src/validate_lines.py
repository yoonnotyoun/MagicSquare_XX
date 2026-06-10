"""Control — 10선 검산 오케스트레이션."""

from src.entity.constants import LINE_IDS, MAGIC_CONSTANT
from src.entity.grid import has_empty_cell
from src.entity.lines import sum_line


def validate_lines(grid: list[list[int]]) -> dict:
    """Control 진입점.

    Returns:
        {"status": "pass"|"fail"|"incomplete", "failed_lines": list[str]}
    """
    if has_empty_cell(grid):
        return {"status": "incomplete", "failed_lines": []}

    failed_lines = [
        line_id
        for line_id in LINE_IDS
        if sum_line(line_id, grid) != MAGIC_CONSTANT
    ]

    if failed_lines:
        return {"status": "fail", "failed_lines": failed_lines}

    return {"status": "pass", "failed_lines": []}
