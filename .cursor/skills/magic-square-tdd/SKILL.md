---
name: magic-square-tdd
description: >-
  MagicSquare_XX validate_lines TDD 사이클(ARRR)을 RED→GREEN→REFACTOR 순서로
  오케스트레이션한다. ARRR, red-test-plan, red-skeleton, tdd-red, green-minimal,
  golden-master, refactor-smell, refactor-safe, validate_lines, pytest, ECB,
  Test Loop, SC-01~03 사용 시 적용한다.
---

# MagicSquare_XX TDD (ARRR)

`validate_lines(grid)` 단위 **1 Test Loop 사이클**을 ARRR Command 체인으로 진행한다.  
각 단계는 `.cursor/commands/`의 전용 Command가 SSOT — 본 Skill은 **순서·게이트·handoff**만 정의한다.

## SSOT

| 문서 | 역할 |
|------|------|
| `.cursorrules` | 도메인·공개 API·ECB·TDD·Mom Test |
| `docs/PRD.md` (있으면) | FR/NFR·Test ID |
| `docs/PRD.md` 없음 | `Report/03_세션3_워크북` §3 SC-01~03 · Test Loop 표 |
| `src/entity/constants.py` | `MAGIC_CONSTANT`, `LINE_IDS` 등 |

## 공개 API (고정)

```python
validate_lines(grid) -> {
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": [...]   # pass·incomplete 시 []
}
```

## ARRR Command 체인

```
/red-test-plan     → Ask     (파일 없음 — C2C·플랜)
/red-skeleton      → Record  (tests/ 골격)
/tdd-red           → Record  (pytest FAILED 확인)
/green-minimal     → Run     (src/ 최소)
/golden-master     → Run     (tests/ pass 기준선)
/refactor-smell    → Review  (냄새 목록, 파일 없음)
/refactor-safe     → Review  (src/ 구조, pytest 유지)
```

**슬래시만 입력** — 각 Command는 추가 질문 없이 채팅·SSOT에서 맥락을 추출한다.

## Phase 선언 (TDD 작업 시 응답 첫 줄)

```
Phase: red | green | refactor | Layer: entity|control|boundary | Track: Logic | Target: validate_lines
```

## 사이클 게이트 (통과 전 다음 Command 금지)

| 단계 | Command | 완료 조건 |
|------|---------|-----------|
| A | `/red-test-plan` | 블록 1~4 표 + 「/red-skeleton 으로 넘길 준비됐다」 |
| R① | `/red-skeleton` | tests/ AAA 골격, src/ 미변경 |
| R② | `/tdd-red` | `pytest` exit ≠ 0 |
| R③ | `/green-minimal` | 대상 테스트 + 전체 `pytest` exit 0 |
| R④ | `/golden-master` | golden pass 테스트 + exit 0 (권장) |
| R⑤ | `/refactor-smell` | S001~S010 표 + handoff |
| R⑥ | `/refactor-safe` | handoff 1~2건, exit 0 |

## Test Loop (불편 우선 — 워크북 기본 순서)

| # | RED 초점 | SC | Layer |
|---|----------|-----|-------|
| 1 | D1·D2 대각선 합 | SC-02 | entity |
| 2 | 10선 일괄 검산 | SC-01 | control |
| 3 | 변경 후 재검산 | SC-03 | control |
| 4 | failed_lines 보고 | SC-02 | entity |
| 5+ | ECB·부분 격자·NFR | R-07 | 구조 리뷰 |

한 사이클 = **요구 1묶음**. assert 완화·skip·xfail·RED 우회 **금지**.

## ECB (리팩터 방향)

| 계층 | 경로 | 역할 |
|------|------|------|
| Entity | `src/entity/` | 선 합·선 ID·상수 |
| Control | `src/validate_lines.py` | 10선 오케스트레이션·status |
| Boundary | (미구현) | 입출력만 — Mom Test 밖 |

## Mom Test 게이트 (R-05)

솔버·UI·자동 채우기·5×5·힌트 등 SC-01~03과 무관한 코드·테스트 **금지**.

## 사이클 마감 체크리스트

- [ ] RED: pytest exit ≠ 0 (`/tdd-red`)
- [ ] GREEN: 최소 구현 (`/green-minimal`)
- [ ] Golden: pass 기준선 (`/golden-master`, 권장)
- [ ] REFACTOR: smell → safe, exit 0
- [ ] (선택) `/export-session` — Report+Prompt 쌍

## git

`commit` / `push`는 **사용자가 명시적으로 요청할 때만**.

## 전체 사이클 한 줄 프롬프트 (재현용)

```
MagicSquare_XX Test Loop 사이클 N — ARRR 순서로 진행:
/red-test-plan → /red-skeleton → /tdd-red → /green-minimal → /golden-master → /refactor-smell → /refactor-safe
SSOT: .cursorrules · docs/PRD.md(또는 Report/03 워크북). 1사이클=1묶음. Mom Test 게이트 준수.
```
