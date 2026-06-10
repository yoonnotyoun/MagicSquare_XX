# Product Requirements Document — MagicSquare_XX

**작성일:** 2026-06-10  
**버전:** 0.1.0  
**상태:** TDD 착수 전 (Harness·스텁만 존재)  
**근거:** [Report/01_MomTest_워크북_MagicSquare_XX.md](../Report/01_MomTest_워크북_MagicSquare_XX.md) · [Report/03_세션3_워크북_MagicSquare_XX.md](../Report/03_세션3_워크북_MagicSquare_XX.md) · [Report/05_세션3_워크북_계약_리뷰_MagicSquare_XX.md](../Report/05_세션3_워크북_계약_리뷰_MagicSquare_XX.md) · [.cursorrules](../.cursorrules)

**문서 계층:** Mom Test → 본 PRD → `.cursorrules`(헌법) → TDD(ARRR) · `src/` · `tests/`

---

## 1. 문제 정의

### 1.1 페르소나

김서연 (2학년, 프로그래밍 기초) — 4×4 **부분 마방진**(빈 칸 2개) 과제. 슬라이드(행·열·대각선 합 34, ECB) 기반, 손 계산 후 코드로 옮기는 흐름.

### 1.2 진짜 문제 (한 문장)

4×4 부분 마방진에서 빈 칸을 채운 뒤 "맞다"고 판정할 때, 행·열은 확인하지만 **대각선 검산을 빠뜨리거나 한쪽만** 보고 멈춰서, 같은 판을 **15~20분** 넘게 다시 검산·숫자 교체를 반복한 뒤에야 틀림을 알게 된다.

### 1.3 Mom Test 증거

| # | 인용 | 시사점 |
|---|------|--------|
| ① | *"행·열만 맞으면 된 줄 알았어. 대각선은 슬라이드에 나왔는데 손 계산할 때는 행·열만 확인하고 넘어간 것 같아."* | 대각선 검산 **누락** |
| ② | *"대각선 하나는 봤는데 반대쪽은 안 봤어. 한쪽만 맞아서 '괜찮겠지' 하고 멈췄거든."* | **양쪽** 대각선 미확인 |
| ③ | *"같은 판에서 빈 칸 근처 숫자만 바꿔 넣어 봤고, 바꾼 뒤에는 행·열·대각선 전부 다시 계산했어."* | 변경 후 **전체 재검산** 필요 |

---

## 2. 목표 (R-G-I-O)

| | |
|---|---|
| **Role** | 4×4 부분 마방진을 손·코드로 다루는 학습자의 **검산 누락·오판**을 줄이기 위해 ECB 기반 마방진 **검산 로직**을 만드는 프로그래머 |
| **Goal** | 빈 칸을 채운 판에 대해 **10선**(행 4 + 열 4 + 대각선 2) 합이 34인지 확인하기 전에는 "완료"로 판정하지 않는다. 틀린 축을 **검산 단계에서** `failed_lines`로 드러낸다. **격자 값이 바뀌면** 호출 측이 `validate_lines`를 **다시 호출**해 10선 전부를 재검산한다 (SC-03). |
| **Input** | 4×4 정수 격자 `grid[4][4]`. 빈 칸 `0`, 채운 칸 `1`~`16` 각 1회. 목표 합 **34**. |
| **Output** | `validate_lines(grid)` 반환 dict — `status`: `pass` \| `fail` \| `incomplete`, `failed_lines`: 선 ID 목록 |

---

## 3. 범위

### 3.1 In Scope (Mom Test · SC-01~03)

- 4×4 격자 **10선** 합 검산 (Logic Track, pytest)
- 공개 API `validate_lines` — Control 단일 진입점
- ECB: Entity(`src/entity/`) · Control(`src/validate_lines.py`)
- TDD: RED → GREEN → REFACTOR (ARRR Command 체인)
- Agent 인프라: `.cursorrules`, `.cursor/commands/`, `.cursor/skills/`

### 3.2 Out of Scope (Mom Test 게이트 · R-05)

| 금지 | 이유 |
|------|------|
| 솔버·자동 채우기 | 빈 칸 해 구하기는 증거 없음 |
| UI·CLI·앱 (Boundary 구현) | 표시만으로 검산 습관 미교정 |
| 5×5 확장·힌트 | SC-01~03 무관 |
| `git commit` / push 자동화 | 사용자 명시 요청 시만 |

---

## 4. 도메인 모델

### 4.1 격자

| 항목 | 값 | SSOT |
|------|-----|------|
| 크기 | 4×4 | `GRID_SIZE = 4` |
| 빈 칸 | `0` | `EMPTY_CELL` |
| 채운 칸 | `1`~`16` 각 1회 | `MIN_CELL`, `MAX_CELL` |
| 마법 상수 | **34** | `MAGIC_CONSTANT` |

상수 정의: `src/entity/constants.py`. 코드·테스트에서 리터럴 `34` **지양**.

### 4.2 10선 (Line ID)

| ID | 의미 | 인덱스 (0-based) |
|----|------|------------------|
| R1~R4 | 1~4행 | `grid[row][0..3]`, row = 0..3 |
| C1~C4 | 1~4열 | `grid[0..3][col]`, col = 0..3 |
| D1 | 주대각선 | `(0,0)(1,1)(2,2)(3,3)` |
| D2 | 반대각선 | `(0,3)(1,2)(2,1)(3,0)` |

- **10선 전부** 검사. 한 축만 검사하고 종료 **금지**.
- 선 ID 목록 SSOT: `LINE_IDS` in `constants.py`.

### 4.3 status 우선순위

1. **`incomplete`** — 격자에 `0`(빈 칸)이 **하나라도** 있으면. `failed_lines = []`. 완료·제출 판정 불가.
2. **`fail`** — 빈 칸 없음, **하나 이상**의 선 합 ≠ `MAGIC_CONSTANT`. 해당 선 ID를 `failed_lines`에 포함 (복수 가능).
3. **`pass`** — 빈 칸 없음, **10선 모두** 합 = `MAGIC_CONSTANT`. `failed_lines = []`.

---

## 5. 기능 요구 (FR)

성공 기준 SC-01~03과 1:1 매핑. C2C·RED 플랜의 **Rule1(PRD FR 인용)** 출처.

| ID | 요구 (FR) | SC | 판정 |
|----|-----------|-----|------|
| **FR-01** | "맞다" 판정 전 **행 4 + 열 4 + 대각선 2 = 10선** 전부 합 34를 검사한다. 행·열만 확인하고 종료할 수 없다. | SC-01 | 10선 누락 시 `pass` 불가 |
| **FR-02** | 주대각선(D1)·반대각선(D2) **둘 다** 합 34를 검사한다. 한쪽만 맞아도 완료로 처리하지 않는다. | SC-02 | D1 또는 D2 불일치 시 `fail`, 해당 ID in `failed_lines` |
| **FR-03** | 한 축이라도 합 ≠ 34이면 완료·제출 판정 금지. **어느 선**이 틀렸는지 `failed_lines`에 선 ID로 반환한다. | SC-02 | `status: fail`, `failed_lines` 비어 있지 않음 |
| **FR-04** | 격자에 빈 칸(`0`)이 있으면 완료 판정 불가. `status: incomplete`, `failed_lines: []`. | — | `.cursorrules` 계약 |
| **FR-05** | 격자 값이 바뀌면 **10선 전부** 다시 검산한다. (단일 API: 변경 후 `validate_lines(grid)` **재호출** — 호출 측·Control 오케스트레이션 책임) | SC-03 | 재호출 시 FR-01~04 재적용 |
| **FR-06** | 10선 모두 합 34이고 빈 칸 없으면 `status: pass`, `failed_lines: []`. | SC-01, SC-02 | golden master 회귀 |

### 5.1 SC ↔ FR 상세

| SC | 성공 기준 | 연결 FR | Mom Test |
|----|-----------|---------|----------|
| **SC-01** | 10선 전체가 검산 목록에 포함 (대각선 누락 방지) | FR-01, FR-06 | ① |
| **SC-02** | 양쪽 대각선 모두 확인; 미통과 축 보고 | FR-02, FR-03 | ② |
| **SC-03** | 숫자 변경 후 10선 전부 재검산 | FR-05 | ③ |

---

## 6. 비기능 요구 (NFR)

| ID | 요구 | 근거 |
|----|------|------|
| **NFR-01** | ECB 책임 분리: Entity(선 합·선 ID) · Control(오케스트레이션·status) · Boundary(입출력만, **미구현**) | R-07 |
| **NFR-02** | Control 진입점 **단일**: `src/validate_lines.py`의 `validate_lines` | Report 05 정합 |
| **NFR-03** | TDD: RED(`tests/`만) → GREEN(최소) → REFACTOR. **1사이클 = FR 1묶음** | R-06 |
| **NFR-04** | RED 우회 금지: assert 완화·`skip`·`xfail`·Domain mock | `.cursorrules` |
| **NFR-05** | Mom Test 게이트: FR-01~06·SC-01~03과 무관한 기능 추가 금지 | R-05 |
| **NFR-06** | pytest로 Logic Track 검증. Python ≥ 3.10 | `pyproject.toml` |
| **NFR-07** | SRP·ECB 유지 REFACTOR; 공개 API 시그니처 변경 금지 | REFACTOR 단계 |

---

## 7. 공개 API (계약)

**정본:** `.cursorrules` 및 본 절. 구현: `src/validate_lines.py` (현재 스텁).

```python
def validate_lines(grid: list[list[int]]) -> dict:
    """Control 진입점.

    Returns:
        {
            "status": "pass" | "fail" | "incomplete",
            "failed_lines": list[str],  # 예: ["R2", "D1"]; pass·incomplete 시 []
        }
    """
```

| `status` | 조건 | `failed_lines` |
|----------|------|----------------|
| `pass` | 10선 합 34, 빈 칸 없음 | `[]` |
| `fail` | 빈 칸 없으나 합 ≠ 34인 선 존재 | 틀린 선 ID (1개 이상) |
| `incomplete` | 빈 칸(`0`) 존재 | `[]` |

**SC-03 해석:** 별도 `verify_after_change` API는 **정의하지 않음**. 격자 변경 후 호출 측이 `validate_lines`를 다시 호출하면 FR-05를 만족한다. Control 내부 캐시·부분 검산 **금지**.

---

## 8. 아키텍처 (ECB)

| 계층 | 경로 | 책임 | Mom Test |
|------|------|------|----------|
| **Entity** | `src/entity/` | 상수, 선 합, 선 ID, (향후) 격자 값 검증 | O |
| **Control** | `src/validate_lines.py` | 10선 일괄 검사, status·`failed_lines` 결정 | O |
| **Boundary** | (없음) | grid 수신·결과 dict 전달만; **검산 로직 금지** | 범위 밖 |

```
grid ──► validate_lines (Control) ──► Entity: sum line, line ID
              │
              └──► { status, failed_lines }
```

---

## 9. Test Loop · Test ID

**불편 우선** (Mom Test 비용·오판 순). ARRR: `/red-test-plan` → … → `/refactor-safe` (`.cursor/skills/magic-square-tdd/SKILL.md`).

| Loop # | RED 초점 | SC | FR | Layer | Test ID (예) |
|--------|----------|-----|-----|-------|--------------|
| 1 | D1·D2 대각선 합 ≠ 34 → `fail` | SC-02 | FR-02, FR-03 | entity | T-D1-01, T-D2-01 |
| 2 | 10선 일괄 — 행·열·대각선 누락 없음 | SC-01 | FR-01 | control | T-10L-01 |
| 3 | `validate_lines` 재호출 = 전체 재검산 | SC-03 | FR-05 | control | T-REVAL-01 |
| 4 | 복수 `failed_lines` (행+대각선 동시) | SC-02 | FR-03 | entity | T-FL-01 |
| 5 | `incomplete` — 빈 칸 `0` | — | FR-04 | control | T-INC-01 |
| 6 | golden master — 10선 pass | SC-01, SC-02 | FR-06 | control | T-GM-01 |
| 7 | ECB·SRP REFACTOR | R-07 | NFR-01, NFR-07 | entity/control | (구조 리뷰) |
| 8 | Mom Test 회귀 — 범위 이탈 없음 | R-05 | NFR-05 | review | (수동·리뷰) |

### 9.1 Test ID 명명

- 접두: `T-` + 축/주제 (예: `T-D1-01`, `T-R2-01`)
- C2C Rule3: Given(4×4 grid) / When(`validate_lines(grid)`) / Then(status, failed_lines)

### 9.2 pytest

```bash
python -m pytest tests/test_validate_lines.py -v
python -m pytest tests/ -v
```

---

## 10. Agent · 문서 SSOT

| 문서·경로 | 역할 |
|-----------|------|
| **본 PRD** | FR/NFR · SC 매핑 · Test Loop · Test ID |
| `.cursorrules` | 도메인·API·ECB·TDD·Mom Test **헌법** (API 정본과 동등) |
| `src/entity/constants.py` | 도메인 상수 SSOT |
| `.cursor/commands/` | ARRR 단계 Command (`red-test-plan`, `tdd-red`, `green-minimal`, …) |
| `.cursor/skills/magic-square-tdd/` | TDD 사이클 오케스트레이션 |
| `.cursor/skills/magic-square-docs/` | Report · Prompt · 체크리스트 템플릿 |
| `Report/` · `Prompt/` | 세션별 보고서·transcript |

---

## 11. 추적성

```
Mom Test (Report/01)
  → R-G-I-O · SC-01~03 (Report/03)
  → validate_lines 계약 (Report/04 · .cursorrules)
  → 계약 정합 리뷰 (Report/05)
  → 본 PRD (FR/NFR · Test Loop · Test ID)
  → TDD ARRR · src/ · tests/
```

| Mom Test | SC | FR | API |
|----------|-----|-----|-----|
| ① 대각선 누락 | SC-01 | FR-01 | 10선 검사 |
| ② 한쪽 대각선만 | SC-02 | FR-02, FR-03 | D1·D2, failed_lines |
| ③ 변경 후 전부 재계산 | SC-03 | FR-05 | validate_lines 재호출 |

---

## 12. 미완 · 다음 단계

- [ ] Test Loop **#1 RED** — T-D1-01 (`/red-test-plan` → `/tdd-red`)
- [ ] GREEN — `src/` 최소 구현 (`/green-minimal`)
- [ ] `.cursorrules` 보완 후보: 10선 좌표·incomplete 우선순위·리터럴 34 금지 명문화 (Report/04 §4)
- [ ] (선택) `docs/DESIGN.md` — Entity 모듈 상세 설계

---

## 부록 A — Golden Master Grid (FR-06 · T-GM-01)

10선 합 34, 1~16 각 1회, 빈 칸 없음:

```python
[
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]
```

기대: `{"status": "pass", "failed_lines": []}`

## 부록 B — Rule (R-01~R-07) 매핑

| Rule | PRD |
|------|-----|
| R-01 | §4.1 도메인 · `EMPTY_CELL` |
| R-02 | FR-01 |
| R-03 | FR-03 |
| R-04 | FR-05 |
| R-05 | §3.2 · NFR-05 |
| R-06 | NFR-03 |
| R-07 | §8 · NFR-01 |
