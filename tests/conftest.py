"""공유 격자 픽스처 — golden master 기준, Test ID별 Arrange 입력."""

import pytest

from src.entity.constants import EMPTY_CELL

# 표준 4×4 마방진 — 10선 합 MAGIC_CONSTANT(34), 1~16 각 1회, 빈 칸 없음
# 16   2   3  13
#  5  11  10   8
#  9   7   6  12
#  4  14  15   1
_GRID_GOLDEN_PASS: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 1],
]


@pytest.fixture
def grid_golden_pass() -> list[list[int]]:
    """T-GM-01 · T-REVAL-01 grid_A — 10선 pass 가능한 완성 마방진."""
    return [row[:] for row in _GRID_GOLDEN_PASS]


@pytest.fixture
def grid_d1_wrong() -> list[list[int]]:
    """T-D1-01 — D1(주대각선) 합 ≠ MAGIC_CONSTANT. golden에서 (0,0)만 조정."""
    grid = [row[:] for row in _GRID_GOLDEN_PASS]
    grid[0][0] = 17  # D1: 17+11+6+1 = 35
    return grid


@pytest.fixture
def grid_d2_wrong() -> list[list[int]]:
    """T-D2-01 — D2(반대각선) 합 ≠ MAGIC_CONSTANT. golden에서 (0,3)만 조정."""
    grid = [row[:] for row in _GRID_GOLDEN_PASS]
    grid[0][3] = 14  # D2: 14+10+7+4 = 35
    return grid


@pytest.fixture
def grid_column_c3_wrong() -> list[list[int]]:
    """T-10L-01 — D1·D2는 합 34, C3 열만 합 ≠ MAGIC_CONSTANT."""
    grid = [row[:] for row in _GRID_GOLDEN_PASS]
    grid[0][2] = 4  # C3: 4+10+6+15 = 35
    return grid


@pytest.fixture
def grid_r2_wrong() -> list[list[int]]:
    """T-REVAL-01 grid_B — golden에서 한 셀 변경해 R2 합 ≠ MAGIC_CONSTANT."""
    grid = [row[:] for row in _GRID_GOLDEN_PASS]
    grid[1][3] = 9  # R2: 5+11+10+9 = 35
    return grid


@pytest.fixture
def grid_r2_and_d1_wrong() -> list[list[int]]:
    """T-FL-01 — R2·D1 동시에 합 ≠ MAGIC_CONSTANT."""
    grid = [row[:] for row in _GRID_GOLDEN_PASS]
    grid[1][1] = 12  # R2: 35, D1: 16+12+6+1 = 35
    return grid


@pytest.fixture
def grid_with_empty_cell() -> list[list[int]]:
    """T-INC-01 — 최소 1칸 EMPTY_CELL(0), 나머지 1~16."""
    grid = [row[:] for row in _GRID_GOLDEN_PASS]
    grid[3][3] = EMPTY_CELL
    return grid
