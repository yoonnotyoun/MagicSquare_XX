# RED Skeleton — 테스트 골격 작성

ARRR **Record(R①)** 전용. `/red-test-plan` 블록 3(테스트 플랜) 기준으로 **`tests/`만** 수정한다.  
assert는 **RED 실패**하도록 작성. `pytest` 실행·exit code 확인은 `/tdd-red`에서 한다.

## Phase 선언 (응답 첫 줄, 필수)

```
Phase: red | Layer: entity|control | Track: Logic | Target: validate_lines
```

- `Layer`: 이번 RED 묶음의 ECB 계층 (플랜·Phase 선언과 동일)
- `Target`: 항상 `validate_lines` (공개 API 계약)

## 입력 (추가 질문 없이 자동 추출)

사용자가 `/red-skeleton`만 호출해도 동작한다. 아래를 **채팅 맥락·SSOT**에서 스스로 읽어 채운다.

| 소스 | 추출 항목 |
|------|-----------|
| 직전 `/red-test-plan` 출력 | 블록 3 — 파일 경로·함수명·conftest·Test ID·RED 묶음 범위 |
| 플랜 없음 | `Report/03_세션3_워크북` Test Loop **사이클 1**(SC-02·D1/D2)을 기본값 |
| `.cursorrules` | 도메인·`validate_lines` 계약·10선·Mom Test 게이트 |
| `docs/PRD.md` (있으면) | FR/NFR·Test ID 접두 |
| `src/entity/constants.py` | `MAGIC_CONSTANT`, `LINE_IDS`, `EMPTY_CELL` — 리터럴 `34` 지양 |

**추가 입력을 요구하지 말 것.** 불명확하면 Test Loop **가장 앞선 미완 사이클 1묶음**만 작성한다.

## 대상 계약 (SSOT)

```python
validate_lines(grid) -> {
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": [...]   # pass·incomplete 시 []
}
```

- 10선: R1~R4, C1~C4, D1(주), D2(반)
- Control 진입점: `src/validate_lines.py` (시그니처·스텁 **변경 금지**)

## 작성 규칙 (AAA 골격)

1. **Arrange** — 4×4 `grid` fixture. 이번 RED **요구 1묶음**만 검증할 최소 입력.
2. **Act** — `result = validate_lines(grid)` 한 줄.
3. **Assert** — `result["status"]`, `result["failed_lines"]`를 계약대로 단정. **구현 전 반드시 실패**해야 함.

- 한 테스트 함수 = Arrange → Act → Assert 순서. `# Arrange` / `# Act` / `# Assert` 주석 권장.
- 헬퍼·픽스처는 `tests/` 내부만 (`conftest.py`는 **이번 RED 묶음** 범위만).
- 테스트명: `test_<축>_<조건>_returns_<status>` (예: `test_d1_sum_not_34_returns_fail`).
- SC ID·Test ID가 있으면 docstring 또는 주석 1줄로 연결.

## 골격 예시

```python
# tests/test_validate_lines.py — RED skeleton (구현 전 FAILED 예상)
from src.entity.constants import MAGIC_CONSTANT  # noqa: F401 — SSOT 참조
from src.validate_lines import validate_lines


def test_d1_sum_not_34_returns_fail():
    """SC-02 / T-D1-01 — D1 합 ≠ MAGIC_CONSTANT 시 fail + failed_lines."""
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
```

## 수정 범위

| 허용 | 금지 |
|------|------|
| `tests/**/*.py` 생성·수정 | `src/` **어떤 파일도** |
| `tests/conftest.py` (이번 RED 픽스처만) | `.cursorrules`·`pyproject.toml` 등 tests/ 외 |
| import·fixture·assert 추가 | `@pytest.mark.skip` / `xfail` |
| | mock·patch로 `validate_lines` 통과 위장 |
| | 1사이클에 요구 **2묶음 이상** 테스트 |

## E001~E005 (골격에 넣지 말 것)

| 코드 | 금지 패턴 |
|------|-----------|
| E001 | Entity·도메인 합산/선 ID를 `mock`·`patch`로 대체 |
| E002 | `validate_lines` 또는 Control을 mock으로 통과 위장 |
| E003 | 10선 중 일부만 검사 (한쪽 축만 assert) |
| E004 | Boundary 테스트에 검산·status 결정 로직 |
| E005 | `skip`·`xfail`·assert 완화·빈 `pass`로 RED 우회 |

## 보고 형식 (스켈레톤 종료 시)

```markdown
## RED Skeleton 보고 — validate_lines

- Phase: red | Layer: … | Track: Logic | Target: validate_lines
- SC/요구: (예: SC-02 — T-D1-01)
- 추가·수정: `tests/…::test_…`
- Arrange 요약: (격자 특성 1줄)
- Assert 요약: status=…, failed_lines=…
- pytest: (아직 미실행 — `/tdd-red`에서 확인)
- 다음: `/tdd-red` — pytest exit ≠ 0 확인
```

## Mom Test 게이트

솔버·UI·자동 채우기·5×5·힌트 등 증거 없는 테스트 금지. 10선·status·failed_lines 계약만.

## 완료 조건

- [ ] Phase 선언 첫 줄
- [ ] 플랜(또는 Test Loop 기본값)의 **Test ID 1묶음**만 `tests/`에 반영
- [ ] AAA 주석·계약 assert 포함
- [ ] `src/`·tests/ 외 파일 미변경
- [ ] E001~E005 패턴 미포함

**완료 한 줄 (응답 마지막, 필수):**

```
/tdd-red 로 RED 확정하자
```

## 다음 단계

1. `/tdd-red` — `python -m pytest … -v` → FAILED (exit ≠ 0) 확인
2. `/green-minimal` — `src/` 최소 구현
