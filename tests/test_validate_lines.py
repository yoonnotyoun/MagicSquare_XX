"""validate_lines 공개 API 테스트 — README Test Plan §9 Test ID 스켈레톤."""

from src.entity.constants import MAGIC_CONSTANT  # noqa: F401 — SSOT 참조
from src.validate_lines import validate_lines


# --- Loop #1 — 대각선 fail (SC-02 · entity) ---


def test_d1_sum_not_magic_constant_returns_fail(grid_d1_wrong):
    """SC-02 / T-D1-01 — D1 합 ≠ MAGIC_CONSTANT 시 fail + failed_lines."""
    # Arrange — 4×4, 빈 칸 없음, D1만 합 ≠ MAGIC_CONSTANT
    grid = grid_d1_wrong

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "fail"
    assert "D1" in result["failed_lines"]


def test_d2_sum_not_magic_constant_returns_fail(grid_d2_wrong):
    """SC-02 / T-D2-01 — D2 합 ≠ MAGIC_CONSTANT 시 fail + failed_lines."""
    # Arrange — 4×4, 빈 칸 없음, D2만 합 ≠ MAGIC_CONSTANT
    grid = grid_d2_wrong

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "fail"
    assert "D2" in result["failed_lines"]


# --- Loop #2 — 10선 일괄 (SC-01 · control) ---


def test_column_fail_when_diagonals_pass(grid_column_c3_wrong):
    """SC-01 / T-10L-01 — 대각선 pass·열 fail 시 10선 검산으로 fail 보고."""
    # Arrange — 4×4, 빈 칸 없음, D1·D2 합 MAGIC_CONSTANT, C3 합 ≠ MAGIC_CONSTANT
    grid = grid_column_c3_wrong

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "fail"
    assert "C3" in result["failed_lines"]


# --- Loop #3 — 재호출 재검산 (SC-03 · control) ---


def test_revalidate_after_grid_change(grid_golden_pass, grid_r2_wrong):
    """SC-03 / T-REVAL-01 — 격자 변경 후 재호출 시 새 격자 기준 전체 재검산."""
    # Arrange — grid_A: pass 가능, grid_B: R2 합 ≠ MAGIC_CONSTANT
    grid_a = grid_golden_pass
    grid_b = grid_r2_wrong

    # Act
    r1 = validate_lines(grid_a)
    r2 = validate_lines(grid_b)

    # Assert
    assert r1["status"] == "pass"
    assert r2["status"] == "fail"
    assert "R2" in r2["failed_lines"]


# --- Loop #4 — 복수 failed_lines (SC-02 · entity) ---


def test_multiple_failed_lines_row_and_diagonal(grid_r2_and_d1_wrong):
    """SC-02 / T-FL-01 — R2·D1 동시 fail 시 failed_lines에 복수 선 ID."""
    # Arrange — 4×4, 빈 칸 없음, R2·D1 합 ≠ MAGIC_CONSTANT
    grid = grid_r2_and_d1_wrong

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "fail"
    assert "R2" in result["failed_lines"]
    assert "D1" in result["failed_lines"]
    assert len(result["failed_lines"]) >= 2


# --- Loop #5 — incomplete (FR-04 · control) ---


def test_empty_cell_returns_incomplete(grid_with_empty_cell):
    """FR-04 / T-INC-01 — 빈 칸(0) 존재 시 incomplete, failed_lines는 []."""
    # Arrange — 4×4, 최소 1칸 EMPTY_CELL(0)
    grid = grid_with_empty_cell

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "incomplete"
    assert result["failed_lines"] == []


# --- Loop #6 — golden master pass (SC-01·02 · FR-06 · control) ---


def test_complete_magic_square_passes_all_ten_lines(grid_golden_pass):
    """SC-01·SC-02 / T-GM-01 — 완성 마방진 10선 pass 회귀 기준선."""
    # Arrange — 4×4 완성 마방진, 10선 합 MAGIC_CONSTANT, 빈 칸 없음
    grid = grid_golden_pass

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "pass"
    assert result["failed_lines"] == []
