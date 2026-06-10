# RED Test Plan — C2C 설계표·테스트 플랜 (Ask)

ARRR **A단계(Ask = RED ③)** 전용. **C2C 설계표·테스트 플랜만** 채팅에 출력한다.  
`tests/`·`src/` **파일 생성·수정 금지**. 실제 테스트 코드는 `/red-skeleton` → `/tdd-red`에서 작성한다.

## Phase 선언 (응답 첫 줄, 필수)

```
Phase: red | Layer: entity|boundary | Track: Logic|UI
```

- `Layer`: 이번 RED 묶음이 검증하는 ECB 계층
  - **entity** — 선 합·선 ID·격자 값
  - **boundary** — 입출력만 (검산 로직 없음). Track A(UI)는 `Layer: boundary`만 바꾸면 본 Command 재사용
- `Track`:
  - **Logic** (Track B) — `validate_lines`·Entity·Control 단위 pytest
  - **UI** (Track A) — Boundary 표시·입출력 (Mom Test 범위 밖이면 플랜에 명시하고 중단 권고)

## 입력 (추가 질문 없이 자동 추출)

사용자가 `/red-test-plan`만 호출해도 동작한다. 아래를 **채팅 맥락·SSOT**에서 스스로 읽어 채운다.

| 소스 | 추출 항목 |
|------|-----------|
| 현재 채팅·최근 Report/Prompt | 세션 주제, 진행 중 SC ID, Test Loop 사이클 번호 |
| `docs/PRD.md` (있으면) | FR/NFR 문구, Test ID 접두 |
| `docs/PRD.md` 없음 | `.cursorrules` 공개 API · `Report/03_세션3_워크북` §3 SC-01~03 · Test Loop 표 |
| `.cursorrules` | 도메인(4×4·0·34·10선)·`validate_lines` 계약·ECB·Mom Test 게이트 |

**추가 입력을 요구하지 말 것.** 불명확하면 SSOT에서 가장 앞선 미완 Test Loop 사이클 1묶음을 기본값으로 쓴다.

## 대상 계약 (SSOT)

```python
validate_lines(grid) -> {
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": [...]   # pass·incomplete 시 []
}
```

- 10선: R1~R4, C1~C4, D1(주), D2(반) — 누락·한쪽만 검사 금지
- 빈 칸 `0` → `incomplete`
- 상수: `src/entity/constants.py` (`MAGIC_CONSTANT`, `LINE_IDS` 등). 리터럴 `34` 지양
- Control 진입점: `src/validate_lines.py`

## C2C Rule 1~3 (설계표 작성 규칙)

| Rule | 의미 | 출력 열 |
|------|------|---------|
| **Rule1** | PRD(또는 SC) **FR 한 줄 인용** — 요구의 출처를 명시 | `PRD FR` |
| **Rule2** | **To-Do 1개** — 1 RED = 요구 1묶음 (혼합 금지) | `To-Do` |
| **Rule3** | **Test ID** + **Given / When / Then** — 실행 가능한 시나리오 | `Test ID`, `Given`, `When`, `Then` |

## 출력 형식 (4블록, 표 필수)

응답 본문은 아래 **4개 블록을 순서대로** 표로 작성한다.

### 블록 1 — C2C 설계표 (Rule1~3)

| PRD FR (인용) | To-Do (1개) | Test ID | Given | When | Then |
|---------------|-------------|---------|-------|------|------|
| (FR 또는 SC-0x 문구) | (이번 사이클 할 일 1문장) | (예: `T-D1-01`) | (4×4 grid 조건) | (`validate_lines(grid)` 호출) | (status·failed_lines 기대) |

### 블록 2 — Track B 표 (Logic)

Track **UI**일 때는 동일 열 구조를 Boundary 대상(함수·컴포넌트)에 맞게 채운다.

| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|---------|-----------|--------------|-----------|----------------------|
| | (`validate_lines` 또는 Entity 함수) | (입력 요약 → 기대 결과 1줄) | (10선·34·ECB 불변식) | (구현 전 `pytest` 실패 유형: AssertionError·NotImplemented 등) |

### 블록 3 — 테스트 플랜

| 항목 | 내용 |
|------|------|
| **파일 경로** | (예: `tests/test_validate_lines.py` 또는 `tests/entity/test_….py`) |
| **함수명** | (예: `test_d1_sum_not_34_returns_fail`) |
| **conftest 픽스처** | (필요 시: `grid_d1_wrong`, `grid_all_filled` 등 — **이번 RED 묶음만**) |
| **pytest 명령** | `python -m pytest <path>::<test_fn> -v` |
| **RED 묶음 범위** | Test ID 목록 + 제외 범위 (다음 사이클·GREEN 항목) |

### 블록 4 — ECB·Mock 점검

Logic Track 기준. **통과(✓) / 위반(✗)** 로 표기.

| 점검 항목 | 결과 | 비고 |
|-----------|------|------|
| Layer·Track이 ECB와 일치 | | |
| Entity 로직을 mock/patch로 대체하지 않음 (Domain Mock 금지) | | |
| `validate_lines` 통과 위장 mock 없음 | | |
| Boundary 테스트에 검산 로직 없음 | | |
| **E001~E005 emit 없음** (아래 위반 패턴 미포함) | | |

**E001~E005 — 플랜·스켈레톤에 넣지 말 것 (emit 금지)**

| 코드 | 금지 패턴 |
|------|-----------|
| E001 | Entity·도메인 합산/선 ID 로직을 `mock`·`patch`로 대체 |
| E002 | `validate_lines` 또는 Control 오케스트레이션을 mock으로 통과 위장 |
| E003 | 10선 중 일부만 검사하는 테스트 (한쪽 축만 assert) |
| E004 | Boundary(UI/CLI) 테스트에 검산·status 결정 로직 포함 |
| E005 | `skip`·`xfail`·assert 완화·빈 `pass`로 RED 우회 |

## Track A (boundary) 재사용

본 Command는 **Track B(Logic)** 기본이다. **Track A(boundary/UI)** 는 다음만 바꾸면 재사용한다.

- Phase 선언: `Layer: boundary | Track: UI`
- 블록 2 대상 함수 → Boundary 입출력 핸들러·표시 계층
- 블록 4 — Mom Test 게이트: UI는 증거 없으면 **플랜 작성 중단** 권고

## 금지 (Ask = RED ③)

| 금지 | 이유 |
|------|------|
| `tests/`·`src/` **파일 생성·수정** | `/red-skeleton`·`/tdd-red` 범위 |
| `src/` 구현·시그니처 변경 | GREEN 범위 |
| GREEN / REFACTOR 단계 작업 | Phase가 red·Ask |
| `@pytest.mark.skip` / `xfail`·assert 완화 제안 | RED 우회 |
| 1사이클에 요구 **2묶음 이상** C2C 행 | 1 RED = 1묶음 |
| Mom Test 밖 기능 (솔버·UI·5×5·힌트) 플랜 포함 | R-05 게이트 |

## Mom Test 게이트

플랜은 SC-01~03·10선 검산·`status`·`failed_lines` 계약과 직접 연결된 것만. 증거 없는 테스트 ID는 넣지 않는다.

## 완료 조건

- [ ] Phase 선언 첫 줄
- [ ] 블록 1~4 표 **전부** 작성
- [ ] Test ID·pytest 경로·RED 묶음 범위가 `/red-skeleton`에 바로 넘길 수 있을 만큼 구체적
- [ ] `tests/`·`src/` 미변경

**완료 한 줄 (응답 마지막, 필수):**

```
/red-skeleton 으로 넘길 준비됐다
```

## ARRR 위치

| ARRR | Command | 파일 변경 |
|------|---------|-----------|
| **A**sk | `/red-test-plan` (본 Command) | 없음 |
| **R**ecord | `/red-skeleton` → `/tdd-red` | `tests/` |
| **R**un | `/green-minimal` → `/golden-master` | `src/` → `tests/` |
| **R**eview | `/refactor-smell` → `/refactor-safe` | smell: 없음 / safe: `src/` |

## 다음 단계

1. `/red-skeleton` — 블록 3 기준 테스트 **골격** (`tests/`, assert는 RED 실패)
2. `/tdd-red` — RED 확정·`pytest` exit ≠ 0 확인
3. `/green-minimal` — `src/` 최소 구현
4. `/golden-master` — pass 회귀 기준선 (권장)
5. `/refactor-smell` → `/refactor-safe` — ECB·SRP 정리
