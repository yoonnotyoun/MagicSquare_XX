# MagicSquare_XX

4×4 부분 마방진에서 **10선(행 4 · 열 4 · 대각선 2) 검산**을 TDD로 구현하는 학습 프로젝트입니다.  
Mom Test로 정의한 검산 누락·오판 문제에 대응하며, 공개 API는 `validate_lines` 하나입니다.

**상태:** TDD 착수 전 — Harness·스텁만 존재 (`validate_lines` 미구현)  
**요구사항 정본:** [docs/PRD.md](docs/PRD.md) · [.cursorrules](.cursorrules)

---

## 문제 (한 문장)

빈 칸을 채운 뒤 "맞다"고 판정할 때 행·열만 보거나 대각선 **한쪽만** 확인해, 같은 판을 15~20분 넘게 재검산하는 불편을 줄인다.

| SC | 성공 기준 |
|----|-----------|
| SC-01 | 10선 전체 검산 (대각선 누락 방지) |
| SC-02 | D1·D2 **양쪽** 대각선 확인 + `failed_lines` 보고 |
| SC-03 | 격자 변경 후 `validate_lines` **재호출**로 10선 재검산 |

---

## 공개 API

```python
from src.validate_lines import validate_lines

result = validate_lines(grid)  # grid: list[list[int]], 4×4
# → {"status": "pass"|"fail"|"incomplete", "failed_lines": [...]}
```

| `status` | 조건 | `failed_lines` |
|----------|------|----------------|
| `pass` | 10선 합 34, 빈 칸 없음 | `[]` |
| `fail` | 빈 칸 없으나 합 ≠ 34인 선 존재 | 틀린 선 ID (예: `["R2", "D1"]`) |
| `incomplete` | 빈 칸 `0` 존재 | `[]` |

- **10선 ID:** R1~R4, C1~C4, D1(주), D2(반) — `src/entity/constants.py`의 `LINE_IDS`
- **도메인:** 4×4, 빈 칸 `0`, 채운 칸 1~16, 마법 상수 34 (`MAGIC_CONSTANT`)

---

## 빠른 시작

**요구:** Python ≥ 3.10, pytest

```bash
# 테스트 (현재는 스텁만 — Test Loop #1 RED 이후 실패·통과 사이클 진행)
python -m pytest tests/ -v
```

---

## 프로젝트 구조

```
MagicSquare_XX/
├── docs/
│   └── PRD.md              # FR/NFR · SC · Test Loop · Test ID
├── src/
│   ├── validate_lines.py   # Control 진입점 (스텁)
│   └── entity/
│       └── constants.py    # GRID_SIZE, MAGIC_CONSTANT, LINE_IDS …
├── tests/
│   └── test_validate_lines.py
├── .cursorrules            # 도메인·API·ECB·TDD 헌법
├── .cursor/
│   ├── commands/           # ARRR 슬래시 Command
│   └── skills/             # TDD · 문서 Skill
├── Report/                 # 세션 보고서
└── Prompt/                 # transcript
```

### ECB

| 계층 | 경로 | 역할 |
|------|------|------|
| Entity | `src/entity/` | 상수, 선 합, 선 ID |
| Control | `src/validate_lines.py` | 10선 오케스트레이션, status 결정 |
| Boundary | (미구현) | 입출력만 — Mom Test 범위 밖 |

---

## TDD (ARRR)

1사이클 = **요구 1묶음**. RED는 `tests/`만, GREEN은 `src/` 최소 구현, REFACTOR는 ECB·SRP 유지.

```
/red-test-plan → /red-skeleton → /tdd-red → /green-minimal → /golden-master → /refactor-smell → /refactor-safe
```

| Command | 단계 |
|---------|------|
| `/red-test-plan` | C2C·테스트 플랜 (파일 없음) |
| `/red-skeleton` · `/tdd-red` | RED — 실패 테스트 |
| `/green-minimal` · `/golden-master` | GREEN — 최소 구현 · pass 기준선 |
| `/refactor-smell` · `/refactor-safe` | REFACTOR |
| `/export-session` | Report + Prompt 쌍 export |

Skill: `.cursor/skills/magic-square-tdd/` · `.cursor/skills/magic-square-docs/`

---

## Test Plan (PRD §9)

**불편 우선** — Mom Test 비용·오판 순으로 Loop #1→#8 진행.  
C2C Rule3: **Given**(4×4 grid) / **When**(`validate_lines(grid)`) / **Then**(`status`, `failed_lines`).  
Test ID 접두: `T-` + 축·주제 (예: `T-D1-01`). 상수는 `src/entity/constants.py` SSOT — 리터럴 `34` 지양.

### Loop 개요

| Loop # | RED 초점 | SC | FR | Layer | Test ID |
|--------|----------|-----|-----|-------|---------|
| 1 | D1·D2 대각선 합 ≠ 34 → `fail` | SC-02 | FR-02, FR-03 | entity | T-D1-01, T-D2-01 |
| 2 | 10선 일괄 — 행·열·대각선 누락 없음 | SC-01 | FR-01 | control | T-10L-01 |
| 3 | `validate_lines` 재호출 = 전체 재검산 | SC-03 | FR-05 | control | T-REVAL-01 |
| 4 | 복수 `failed_lines` (행+대각선 동시) | SC-02 | FR-03 | entity | T-FL-01 |
| 5 | `incomplete` — 빈 칸 `0` | — | FR-04 | control | T-INC-01 |
| 6 | golden master — 10선 pass | SC-01, SC-02 | FR-06 | control | T-GM-01 |
| 7 | ECB·SRP REFACTOR | R-07 | NFR-01, NFR-07 | entity/control | (구조 리뷰) |
| 8 | Mom Test 회귀 — 범위 이탈 없음 | R-05 | NFR-05 | review | (수동·리뷰) |

**공통 파일:** `tests/test_validate_lines.py`  
**공통 실행:** `python -m pytest tests/test_validate_lines.py -v`

---

### Loop #1 — 대각선 `fail` (SC-02 · entity)

| PRD FR | To-Do | Test ID | Given | When | Then |
|--------|-------|---------|-------|------|------|
| FR-02: 주·반대각선 **둘 다** 합 34 검사 | D1만 틀린 채워진 격자로 대각선 fail 검증 | **T-D1-01** | 4×4, 빈 칸 없음, 행·열·D2는 합 `MAGIC_CONSTANT`, **D1만** 합 ≠ 34 | `validate_lines(grid)` | `status == "fail"`, `"D1" in failed_lines` |
| FR-02: 한쪽만 맞아도 완료 불가 | D2만 틀린 채워진 격자로 반대각선 fail 검증 | **T-D2-01** | 4×4, 빈 칸 없음, 행·열·D1은 합 `MAGIC_CONSTANT`, **D2만** 합 ≠ 34 | `validate_lines(grid)` | `status == "fail"`, `"D2" in failed_lines` |

| Test ID | 함수명 (예) | Expected RED Failure |
|---------|-------------|----------------------|
| T-D1-01 | `test_d1_sum_not_magic_constant_returns_fail` | AssertionError 또는 NotImplemented (스텁) |
| T-D2-01 | `test_d2_sum_not_magic_constant_returns_fail` | 동일 |

**픽스처 (예):** `grid_d1_wrong`, `grid_d2_wrong` — golden master(아래 Loop #6)에서 D1/D2 셀만 조정해 구성.

---

### Loop #2 — 10선 일괄 (SC-01 · control)

| PRD FR | To-Do | Test ID | Given | When | Then |
|--------|-------|---------|-------|------|------|
| FR-01: 행 4 + 열 4 + 대각선 2 = **10선 전부** 검사 | 대각선은 맞고 **열**만 틀린 격자로 행·열 검산 포함 확인 | **T-10L-01** | 4×4, 빈 칸 없음, D1·D2 합 34, **C3**(또는 임의 열) 합 ≠ 34 | `validate_lines(grid)` | `status == "fail"`, `"C3" in failed_lines` (해당 열 ID) |

| Test ID | 함수명 (예) | Invariant | Expected RED Failure |
|---------|-------------|-----------|----------------------|
| T-10L-01 | `test_column_fail_when_diagonals_pass` | 10선 중 **한 축**이라도 ≠ 34이면 `pass` 불가 | AssertionError |

**의도:** 대각선만 검사하는 구현이면 `pass`로 오판 → RED로 잡음.

---

### Loop #3 — 재호출 재검산 (SC-03 · control)

| PRD FR | To-Do | Test ID | Given | When | Then |
|--------|-------|---------|-------|------|------|
| FR-05: 격자 변경 후 `validate_lines` **재호출**로 10선 전부 재검산 | 동일 호출 측에서 grid 변경 후 두 번째 호출 결과가 **새 격자** 기준 | **T-REVAL-01** | (1) grid_A: 10선 pass 가능한 채워진 격자 → (2) grid_B: grid_A에서 한 셀 변경해 R2 합 ≠ 34 | `r1 = validate_lines(grid_A)` 후 `r2 = validate_lines(grid_B)` | `r1["status"] == "pass"`, `r2["status"] == "fail"`, `"R2" in r2["failed_lines"]` |

| Test ID | 함수명 (예) | Invariant | Expected RED Failure |
|---------|-------------|-----------|----------------------|
| T-REVAL-01 | `test_revalidate_after_grid_change` | Control 내부 캐시·부분 검산 **금지** — 매 호출 전체 10선 | AssertionError |

---

### Loop #4 — 복수 `failed_lines` (SC-02 · entity)

| PRD FR | To-Do | Test ID | Given | When | Then |
|--------|-------|---------|-------|------|------|
| FR-03: 틀린 선 ID를 `failed_lines`에 반환 (복수 가능) | 행과 대각선이 **동시에** 틀린 격자 | **T-FL-01** | 4×4, 빈 칸 없음, **R2** 합 ≠ 34 **且** **D1** 합 ≠ 34 | `validate_lines(grid)` | `status == "fail"`, `"R2" in failed_lines`, `"D1" in failed_lines`, `len(failed_lines) >= 2` |

| Test ID | 함수명 (예) | Expected RED Failure |
|---------|-------------|----------------------|
| T-FL-01 | `test_multiple_failed_lines_row_and_diagonal` | AssertionError (한 축만 보고하는 구현) |

---

### Loop #5 — `incomplete` (FR-04 · control)

| PRD FR | To-Do | Test ID | Given | When | Then |
|--------|-------|---------|-------|------|------|
| FR-04: 빈 칸 `0` 존재 시 완료 판정 불가 | 빈 칸 1개 이상인 격자 | **T-INC-01** | 4×4, **최소 1칸** `EMPTY_CELL`(0), 나머지는 1~16 | `validate_lines(grid)` | `status == "incomplete"`, `failed_lines == []` |

| Test ID | 함수명 (예) | Invariant | Expected RED Failure |
|---------|-------------|-----------|----------------------|
| T-INC-01 | `test_empty_cell_returns_incomplete` | `incomplete` 시 `failed_lines`는 **항상** `[]` | AssertionError |

**우선순위:** 빈 칸이 있으면 합 검사 전 `incomplete` (FR-04 > FR-03).

---

### Loop #6 — golden master `pass` (SC-01·02 · FR-06 · control)

| PRD FR | To-Do | Test ID | Given | When | Then |
|--------|-------|---------|-------|------|------|
| FR-06: 10선 모두 34, 빈 칸 없으면 `pass` | 표준 4×4 마방진 전체 | **T-GM-01** | 4×4 완성 마방진 (1~16 각 1회, 빈 칸 없음, 10선 합 = `MAGIC_CONSTANT`) | `validate_lines(grid)` | `status == "pass"`, `failed_lines == []` |

**golden master grid (참고):**

```
16   2   3  13
 5  11  10   8
 9   7   6  12
 4  14  15   1
```

| Test ID | 함수명 (예) | 역할 |
|---------|-------------|------|
| T-GM-01 | `test_complete_magic_square_passes_all_ten_lines` | GREEN 회귀 기준선 — 이후 REFACTOR에서도 유지 |

---

### Loop #7 — ECB·SRP REFACTOR (NFR-01, NFR-07)

코드 테스트 ID 없음. **구조 리뷰** 체크리스트:

| 점검 | 기대 |
|------|------|
| Entity | 선 합·선 ID·상수가 `src/entity/`에만 존재 |
| Control | `validate_lines.py`는 오케스트레이션·status 결정만 |
| SRP | Entity 함수 단일 책임, Control에 합산 로직 혼입 없음 |
| API | `validate_lines` 시그니처·반환 dict 형태 불변 |
| pytest | Loop #1~#6 전부 green 유지 |

Command: `/refactor-smell` → `/refactor-safe`

---

### Loop #8 — Mom Test 회귀 (NFR-05)

수동·리뷰. **범위 이탈 없음** 확인:

- 솔버·자동 채우기·UI·5×5·힌트 미추가
- 공개 API `validate_lines` 단일 유지
- SC-01~03·FR-01~06 추적성 유지 ([PRD §11](docs/PRD.md#11-추적성))

---

### ECB·Mock 점검 (Logic Track 공통)

| 점검 | 요구 |
|------|------|
| Domain Mock 금지 (E001) | Entity 합산·선 ID를 `mock`/`patch`로 대체하지 않음 |
| 통과 위장 금지 (E002) | `validate_lines`를 mock으로 pass 처리하지 않음 |
| 10선 전부 (E003) | 한 축만 assert하는 테스트로 RED 우회 금지 |
| RED 우회 금지 (E005) | `skip`·`xfail`·assert 완화·빈 `pass` 금지 |

---

### 진행 상태

| Loop | Test ID | 상태 |
|------|---------|------|
| 1 | T-D1-01, T-D2-01 | **다음 RED** |
| 2 | T-10L-01 | 대기 |
| 3 | T-REVAL-01 | 대기 |
| 4 | T-FL-01 | 대기 |
| 5 | T-INC-01 | 대기 |
| 6 | T-GM-01 | 대기 |
| 7 | (구조 리뷰) | 대기 |
| 8 | (수동·리뷰) | 대기 |

정본: [docs/PRD.md §9](docs/PRD.md#9-test-loop--test-id)

---

## 범위 밖 (Mom Test 게이트)

솔버, 자동 채우기, UI/CLI, 5×5 확장, 힌트 등 SC-01~03과 무관한 기능은 **추가하지 않습니다**.

---

## 문서

| 문서 | 내용 |
|------|------|
| [docs/PRD.md](docs/PRD.md) | FR/NFR, 도메인, Test Loop, Test ID |
| [.cursorrules](.cursorrules) | 프로젝트 헌법 (API·ECB·TDD) |
| [Report/03_세션3_워크북_MagicSquare_XX.md](Report/03_세션3_워크북_MagicSquare_XX.md) | Mom Test · R-G-I-O · 워크북 |
| [Report/05_세션3_워크북_계약_리뷰_MagicSquare_XX.md](Report/05_세션3_워크북_계약_리뷰_MagicSquare_XX.md) | `validate_lines` 계약 정합 리뷰 |
| [Report/06_세션4_TestPlan_README_MagicSquare_XX.md](Report/06_세션4_TestPlan_README_MagicSquare_XX.md) | PRD §9 Test Plan · README 갱신 |

```
Mom Test → 워크북(세션 3) → .cursorrules → PRD → Test Plan(세션 4) → TDD(ARRR) → src/ · tests/
```
