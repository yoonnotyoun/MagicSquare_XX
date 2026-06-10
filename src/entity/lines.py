"""Entity — 10선 합 계산."""

from src.entity.constants import GRID_SIZE


def sum_line(line_id: str, grid: list[list[int]]) -> int:
    """선 ID에 해당하는 4칸 합을 반환한다."""
    if line_id.startswith("R"):
        row = int(line_id[1]) - 1
        return sum(grid[row])
    if line_id.startswith("C"):
        col = int(line_id[1]) - 1
        return sum(grid[r][col] for r in range(GRID_SIZE))
    if line_id == "D1":
        return sum(grid[i][i] for i in range(GRID_SIZE))
    if line_id == "D2":
        return sum(grid[i][GRID_SIZE - 1 - i] for i in range(GRID_SIZE))
    raise ValueError(f"unknown line_id: {line_id!r}")
