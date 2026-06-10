# Golden Master — pass 기준선 회귀

ARRR **Run(R③)** 전용. **유효 4×4 마방진(10선 합 34)** golden fixture로 `status: pass` **회귀 기준선**을 `tests/`에 추가한다.  
`src/`는 **수정하지 않는다** (이미 GREEN 통과 상태 전제). 실패 시 `/green-minimal`로 돌아간다.

## Phase 선언 (응답 첫 줄, 필수)

```
Phase: green | Layer: entity|control | Track: Logic | Target: validate_lines
```

- Golden master는 GREEN 직후 **회귀 안전망** — REFACTOR 전 pass 기준선 고정

## 입력 (추가 질문 없이 자동 추출)

사용자가 `/golden-master`만 호출해도 동작한다.

| 소스 | 추출 항목 |
|------|-----------|
| 직전 GREEN 보고·pytest | 통과한 Entity/Control 범위 |
| `src/entity/constants.py` | `MAGIC_CONSTANT`, `LINE_IDS`, `GRID_SIZE` |
| `.cursorrules` | pass 조건 — 10선·빈 칸 없음 |
| `tests/conftest.py` (있으면) | 기존 fixture 명명 규칙 |

**추가 입력을 요구하지 말 것.** 표준 4×4 마방진(1~16 각 1회)을 기본 golden grid로 쓴다.

## Golden Grid (기본 SSOT)

아래는 **10선 합 34**·1~16 각 1회·빈 칸 없음을 만족하는 기본 golden master:

```python
GOLDEN_GRID = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]
```

- fixture명: `grid_golden_pass` (또는 `conftest.py`의 `@pytest.fixture`로 공유)
- 테스트명: `test_golden_grid_all_lines_pass` (또는 `test_golden_master_returns_pass`)
- SC 연결: SC-01(10선 포함)·SC-02(양쪽 대각선) 회귀

## 작성 규칙

1. **tests/만** 수정 — `tests/test_validate_lines.py` 또는 `tests/conftest.py` + 테스트.
2. **Assert (최소)**:
   - `result["status"] == "pass"`
   - `result["failed_lines"] == []`
3. **10선 암시 검증** — golden grid 자체가 10선=34임을 주석으로 명시. 한 축만 assert하지 않는다 (E003).
4. **incomplete golden은 별도 사이클** — 빈 칸(`0`) 포함 pass 테스트는 해당 RED 사이클에서만.

## pytest

```bash
python -m pytest tests/test_validate_lines.py::test_golden_master_returns_pass -v
python -m pytest tests/ -v
```

**완료 조건:** golden 테스트 PASSED + 전체 pytest exit 0.

## 보고 형식

```markdown
## Golden Master 보고 — validate_lines

- Phase: green | Layer: … | Track: Logic | Target: validate_lines
- Golden fixture: `grid_golden_pass` (10선=34, 1~16)
- 추가 테스트: `tests/…::test_golden_master_returns_pass`
- pytest: exit 0 ✓
- 다음: `/refactor-smell` — REFACTOR 전 냄새 점검
```

## 금지

| 금지 | 이유 |
|------|------|
| `src/` 수정 | GREEN·REFACTOR 분리 |
| golden grid를 **부분 축만** 맞는 격자로 사용 | E003 — 10선 기준선 아님 |
| assert 완화·skip·xfail | 우회 |
| 솔버로 grid **생성** 로직을 src/에 추가 | Mom Test 범위 밖 |
| 1~16 중복·누락 grid | 도메인 위반 |

## Mom Test 게이트

pass 기준선은 **검산 계약** 회귀용. 솔버·UI·힌트와 무관.

## 완료 조건

- [ ] Phase 선언 첫 줄
- [ ] golden fixture + pass assert 테스트 추가
- [ ] `src/` 미변경
- [ ] 전체 pytest exit 0

**완료 한 줄 (응답 마지막, 필수):**

```
/refactor-smell 로 REFACTOR 준비하자
```

## 다음 단계

1. `/refactor-smell` — ECB·SRP 냄새 목록 (Ask, 파일 미변경)
2. `/refactor-safe` — 냄새 제거·구조 정리 (pytest 유지)
