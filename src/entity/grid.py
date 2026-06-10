"""Entity — 격자 상태."""

from src.entity.constants import EMPTY_CELL


def has_empty_cell(grid: list[list[int]]) -> bool:
    """빈 칸(EMPTY_CELL) 존재 여부."""
    return any(cell == EMPTY_CELL for row in grid for cell in row)
