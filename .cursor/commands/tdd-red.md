# TDD RED — validate_lines

`validate_lines(grid)` RED 단계 전용. **tests/만** 수정한다.

## Phase 선언 (응답 첫 줄, 필수)

```
Phase: red | Layer: entity|control | Track: Logic | Target: validate_lines
```

- `Layer`: 이번 사이클이 검증하는 ECB 계층 (Entity: 선 합·선 ID / Control: status·failed_lines 오케스트레이션)
- `Target`: 항상 `validate_lines` (공개 API 계약 기준)

## 대상 계약 (.cursorrules)

```python
validate_lines(grid) -> {
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": [...]   # pass·incomplete 시 []
}
```

- 도메인: 4×4, 빈 칸 `0`, 1~16, 마법상수 34, 10선(R1~R4·C1~C4·D1·D2)
- 상수 참조: `src/entity/constants.py`의 `MAGIC_CONSTANT`, `LINE_IDS` 등 (리터럴 `34` 지양)

## AAA 절차

1. **Arrange** — 4×4 `grid` fixture 준비. 이번 사이클 **요구 1묶음**만 검증할 최소 입력.
2. **Act** — `result = validate_lines(grid)` 호출.
3. **Assert** — `result["status"]`, `result["failed_lines"]`를 계약대로 단정. Mom Test·SC ID와 연결 가능하면 테스트명·주석에 표기.

한 테스트 함수 = Arrange → Act → Assert 순서. 헬퍼는 `tests/` 내부만.

## pytest 예시

```bash
# 전체
python -m pytest tests/test_validate_lines.py -v

# 이번 사이클 테스트만
python -m pytest tests/test_validate_lines.py::test_d1_sum_not_34_returns_fail -v
```

```python
# tests/test_validate_lines.py — RED 예시 (구현 전 실패해야 함)
from src.entity.constants import MAGIC_CONSTANT
from src.validate_lines import validate_lines


def test_d1_sum_not_34_returns_fail():
    # Arrange — D1(주대각선)만 34가 아닌 4×4 격자
    grid = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
    ]

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "fail"
    assert "D1" in result["failed_lines"]
    assert result["status"] != "pass"  # SC-02: 한쪽만 맞아도 pass 금지
```

**RED 완료 조건:** 위와 같이 **새 테스트가 실패**하고, `pytest` exit code ≠ 0.

## 보고 형식 (RED 종료 시)

```markdown
## RED 보고 — validate_lines

- Phase: red | Layer: … | Track: Logic | Target: validate_lines
- SC/요구: (예: SC-02 — D1 합 ≠ 34 시 fail + failed_lines)
- 추가 테스트: `tests/test_validate_lines.py::test_…`
- Arrange 요약: (격자 특성 1줄)
- Assert 요약: status=…, failed_lines=…
- pytest: `python -m pytest … -v` → FAILED (exit ≠ 0) ✓
- 다음: `/green-minimal` — src/ 최소 구현
```

## 금지 (RED)

| 금지 | 이유 |
|------|------|
| `src/` **어떤 파일도** 수정 | GREEN 범위. 시그니처·`...` 스텁 포함 |
| assert 완화·삭제·조건 느슨화 | RED 우회 |
| `@pytest.mark.skip` / `xfail` | RED 우회 |
| mock·patch로 `validate_lines` 통과 위장 | 실제 구현 없이 GREEN 처리 |
| `.cursorrules`·`pyproject.toml` 등 tests/ 외 수정 | RED 범위 이탈 |
| 1사이클에 요구 **2묶음 이상** 혼합 | 1 RED = 요구 1묶음 |

## Mom Test 게이트

솔버·UI·자동 채우기·5×5 등 증거 없는 테스트 추가 금지. 10선 검산·status·failed_lines 계약만.
