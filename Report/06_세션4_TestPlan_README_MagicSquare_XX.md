# 세션 4 — PRD Test Loop 테스트 플랜 · README 갱신 — MagicSquare_XX

**작성일:** 2026-06-10  
**근거:** [docs/PRD.md §9](../docs/PRD.md#9-test-loop--test-id) · [05_세션3_워크북_계약_리뷰_MagicSquare_XX.md](05_세션3_워크북_계약_리뷰_MagicSquare_XX.md) · [.cursorrules](../.cursorrules)  
**관련 프롬프트:** `Prompt/06_세션4_TestPlan_README_프롬프트.md`

---

## 1) 세션 목적

PRD §9 Test Loop 8개·Test ID에 대한 **C2C 테스트 플랜**을 작성하고, 프로젝트 진입점인 `README.md`에 Test Plan 섹션으로 반영한다. TDD RED 착수 전 **실행 가능한 시나리오 SSOT**를 README에 고정한다.

---

## 2) 사용자 요청 요약

| # | 요청 | 결과 |
|---|------|------|
| 1 | `@PRD.md (176-194)` 테스트 내용에 대한 테스트 플랜 작성 + `README.md` 업데이트 | `README.md`에 **Test Plan (PRD §9)** 섹션 추가 (Loop #1~#8) |
| 2 | `/export-session` | Report·Prompt `06`번 쌍 생성 |
| 3 | 세션 번호 정정 — **세션 4** | 파일명·본문 `세션3` → `세션4` 반영 |

---

## 3) 산출물 목록

| 경로 | 역할 |
|------|------|
| `README.md` | Test Plan 섹션 신규 — Loop 개요·C2C Given/When/Then·함수명 예·ECB 점검·진행 상태 |
| `Report/06_세션4_TestPlan_README_MagicSquare_XX.md` | 본 보고서 |
| `Prompt/06_세션4_TestPlan_README_프롬프트.md` | 대화 transcript |

**변경 없음:** `tests/` · `src/` · `.cursorrules` · `docs/PRD.md`

---

## 4) 주요 결정·계약

### Test Plan 구조 (README)

- **Loop 개요 표** — PRD §9와 동일 매핑 (SC · FR · Layer · Test ID)
- **Loop #1~#6** — C2C Rule3: Given(4×4 grid) / When(`validate_lines(grid)`) / Then(`status`, `failed_lines`)
- **Loop #7~#8** — pytest Test ID 없음; REFACTOR·Mom Test 회귀 체크리스트
- **ECB·Mock 점검** — E001~E005 금지 패턴 (Logic Track 공통)
- **진행 상태** — Loop #1 (`T-D1-01`, `T-D2-01`) = **다음 RED**

### Test ID · Loop 매핑 (요약)

| Loop | Test ID | RED 초점 |
|------|---------|----------|
| 1 | T-D1-01, T-D2-01 | D1·D2 대각선 합 ≠ 34 → `fail` |
| 2 | T-10L-01 | 10선 일괄 (열 fail, 대각선 pass) |
| 3 | T-REVAL-01 | 재호출 = 전체 재검산 (캐시 금지) |
| 4 | T-FL-01 | 복수 `failed_lines` (행+대각선) |
| 5 | T-INC-01 | 빈 칸 `0` → `incomplete` |
| 6 | T-GM-01 | golden master 10선 `pass` |
| 7 | (구조 리뷰) | ECB·SRP REFACTOR |
| 8 | (수동·리뷰) | Mom Test 범위 회귀 |

### golden master (Loop #6 참고 격자)

표준 4×4 마방진 — README에 grid 예시 포함. Loop #1 픽스처(`grid_d1_wrong`, `grid_d2_wrong`)는 이 격자에서 D1/D2 셀만 조정해 구성하도록 명시.

### 도메인·API (불변)

- 공개 API: `validate_lines(grid)` → `{ status, failed_lines }`
- 10선: R1~R4, C1~C4, D1, D2 — `src/entity/constants.py` `LINE_IDS`
- 상수 SSOT: `MAGIC_CONSTANT`, `EMPTY_CELL` 등 — 리터럴 `34` 지양
- ECB: Entity(선 합·ID) · Control(오케스트레이션) · Boundary 미구현

---

## 5) 미완·다음 단계 체크리스트

- [ ] `/red-skeleton` — Loop #1 `T-D1-01` 테스트 골격 (`tests/test_validate_lines.py`)
- [ ] `/tdd-red` — RED 확정 · `pytest` exit ≠ 0
- [ ] `/green-minimal` — 대각선 fail 최소 구현
- [ ] Loop #2~#6 순차 RED → GREEN
- [ ] `/golden-master` — `T-GM-01` 회귀 기준선
- [ ] `/refactor-smell` → `/refactor-safe` — Loop #7

---

## 6) 문서 추적성

```
Mom Test → 워크북 (세션 3) → .cursorrules → PRD §9 Test Loop
  → 05_계약_리뷰 (세션 3 마감)
  → 본 세션 4: README Test Plan SSOT (Loop #1~#8 C2C)
  → Prompt/06_세션4_TestPlan_README_프롬프트.md
  → (다음) /red-skeleton — T-D1-01 RED
```
