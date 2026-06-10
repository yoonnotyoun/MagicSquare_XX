"""4×4 마방진 검산 PyQt 데모 — Boundary만 담당, 검산은 validate_lines에 위임."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.entity.constants import EMPTY_CELL, GRID_SIZE
from src.validate_lines import validate_lines

# conftest golden master와 동일
_SAMPLE_PASS: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, 1],
]

_SAMPLE_INCOMPLETE: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 6, 12],
    [4, 14, 15, EMPTY_CELL],
]

_STATUS_STYLE = {
    "pass": "color: #1b7f3a; font-weight: bold;",
    "fail": "color: #b3261e; font-weight: bold;",
    "incomplete": "color: #9a6700; font-weight: bold;",
}

_STATUS_LABEL = {
    "pass": "pass — 10선 모두 합 34",
    "fail": "fail — 틀린 선",
    "incomplete": "incomplete — 빈 칸(0)이 있습니다",
}


def _format_cell(value: int) -> str:
    return "" if value == EMPTY_CELL else str(value)


def _parse_cell(text: str) -> int | None:
    stripped = text.strip()
    if stripped == "":
        return EMPTY_CELL
    try:
        return int(stripped)
    except ValueError:
        return None


class MagicSquareWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MagicSquare_XX — validate_lines 데모")
        self.setMinimumSize(420, 360)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        hint = QLabel("4×4 격자 (빈 칸은 0 또는 비움). 검산 버튼으로 validate_lines 호출.")
        hint.setWordWrap(True)
        root.addWidget(hint)

        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(6)

        mono = QFont("Consolas", 14)
        mono.setStyleHint(QFont.StyleHint.Monospace)
        self._cells: list[list[QLineEdit]] = []
        for row in range(GRID_SIZE):
            row_cells: list[QLineEdit] = []
            for col in range(GRID_SIZE):
                cell = QLineEdit()
                cell.setFont(mono)
                cell.setMaxLength(2)
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setFixedSize(52, 40)
                cell.setPlaceholderText("0")
                grid_layout.addWidget(cell, row, col)
                row_cells.append(cell)
            self._cells.append(row_cells)

        root.addWidget(grid_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        button_row = QHBoxLayout()
        self._btn_validate = QPushButton("검산")
        self._btn_validate.clicked.connect(self._on_validate)
        self._btn_sample_pass = QPushButton("샘플: 완성")
        self._btn_sample_pass.clicked.connect(lambda: self._load_grid(_SAMPLE_PASS))
        self._btn_sample_incomplete = QPushButton("샘플: 빈 칸")
        self._btn_sample_incomplete.clicked.connect(
            lambda: self._load_grid(_SAMPLE_INCOMPLETE)
        )
        self._btn_clear = QPushButton("초기화")
        self._btn_clear.clicked.connect(self._on_clear)
        for btn in (
            self._btn_validate,
            self._btn_sample_pass,
            self._btn_sample_incomplete,
            self._btn_clear,
        ):
            button_row.addWidget(btn)
        root.addLayout(button_row)

        self._result = QLabel("격자를 입력한 뒤 [검산]을 누르세요.")
        self._result.setWordWrap(True)
        root.addWidget(self._result)

        self._load_grid(_SAMPLE_INCOMPLETE)

    def _load_grid(self, grid: list[list[int]]) -> None:
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self._cells[row][col].setText(_format_cell(grid[row][col]))
        self._result.setText("격자를 불러왔습니다. [검산]을 누르세요.")
        self._result.setStyleSheet("")

    def _on_clear(self) -> None:
        for row in self._cells:
            for cell in row:
                cell.clear()
        self._result.setText("격자를 입력한 뒤 [검산]을 누르세요.")
        self._result.setStyleSheet("")

    def _read_grid(self) -> list[list[int]] | None:
        grid: list[list[int]] = []
        for row in range(GRID_SIZE):
            row_values: list[int] = []
            for col in range(GRID_SIZE):
                value = _parse_cell(self._cells[row][col].text())
                if value is None:
                    QMessageBox.warning(
                        self,
                        "입력 오류",
                        f"({row + 1}행, {col + 1}열)에는 0~16 정수만 입력할 수 있습니다.",
                    )
                    return None
                row_values.append(value)
            grid.append(row_values)
        return grid

    def _on_validate(self) -> None:
        grid = self._read_grid()
        if grid is None:
            return

        result = validate_lines(grid)
        status = result["status"]
        failed = result["failed_lines"]

        if status == "fail" and failed:
            detail = f"{_STATUS_LABEL[status]}: {', '.join(failed)}"
        else:
            detail = _STATUS_LABEL[status]

        self._result.setText(detail)
        self._result.setStyleSheet(_STATUS_STYLE.get(status, ""))


def main() -> int:
    app = QApplication(sys.argv)
    window = MagicSquareWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
