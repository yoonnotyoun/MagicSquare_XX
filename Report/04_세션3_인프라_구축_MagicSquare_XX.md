# 세션 3 인프라 구축 — MagicSquare_XX

**작성일:** 2026-06-10  
**근거:** [03_세션3_워크북_MagicSquare_XX.md](03_세션3_워크북_MagicSquare_XX.md) · [.cursorrules](../.cursorrules)  
**관련 프롬프트:** `Prompt/04_세션3_인프라_구축_프롬프트.md`

---

## 1) 세션 목적

세션 3 워크북(§5 Rule·Command·Test Loop)에 따라 **TDD 착수 전 Agent 인프라**를 코드·규칙·Command 수준까지 구축한다. 구현(GREEN)은 범위 밖 — **하네스 골격·헌법·RED Command**만 완료.

---

## 2) 사용자 요청 요약

| # | 요청 | 결과 |
|---|------|------|
| 1 | 최소 Harness (pytest, `validate_lines` 시그니처, 빈 tests) | `pyproject.toml`, `src/`, `tests/` 골격 |
| 2 | `.cursorrules` 초안 40~60줄 (도메인·API·ECB·TDD·AI) | `.cursorrules` (56줄) |
| 3 | Harness를 `.cursorrules` 기반 갱신 | ECB `entity/constants.py`, Control 시그니처·docstring |
| 4 | `.cursorrules` 빠진 규칙 점검 (Ask) | 10선·SSOT·incomplete·RED 금지 표 (파일 미변경) |
| 5 | `tdd-red.md` Command (validate_lines RED 전용) | `.cursor/commands/tdd-red.md` |
| 6 | `export-session.md` + 이번 대화 export | 본 Report·Prompt·Command |

---

## 3) 산출물 목록

| 경로 | 역할 |
|------|------|
| `pyproject.toml` | pytest 설정 (`testpaths`, `pythonpath`) |
| `src/__init__.py` | 패키지 (빈 파일) |
| `src/validate_lines.py` | **Control** 진입점 — `validate_lines(grid) -> dict` 스텁 |
| `src/entity/__init__.py` | Entity 패키지 |
| `src/entity/constants.py` | 도메인 SSOT 후보: `GRID_SIZE`, `MAGIC_CONSTANT`, `LINE_IDS` 등 |
| `tests/__init__.py` | 테스트 패키지 |
| `tests/test_validate_lines.py` | import만 (테스트 본문 없음) |
| `.cursorrules` | 프로젝트 헌법 — 10선·API·ECB·TDD·Mom Test 게이트 |
| `.cursor/commands/tdd-red.md` | RED 단계 Command (Phase·AAA·pytest·금지) |
| `.cursor/commands/export-session.md` | 세션 export Command (Report+Prompt 쌍) |

---

## 4) 주요 결정·계약

### 도메인

- 4×4 격자, 빈 칸 `0`, 채운 칸 `1`~`16`, 마법상수 **34**
- 검산 **10선**: R1~R4, C1~C4, D1(주), D2(반) — 누락·한쪽만 검사 금지

### 공개 API

```python
validate_lines(grid) -> {
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": [...]   # pass·incomplete 시 []
}
```

| status | 조건 |
|--------|------|
| `pass` | 10선 합 34, 빈 칸 없음 |
| `fail` | 빈 칸 없으나 합 ≠ 34인 선 → `failed_lines`에 선 ID |
| `incomplete` | 빈 칸(`0`) 존재 → 완료 판정 불가 |

### ECB

| 계층 | 위치 | 역할 |
|------|------|------|
| Entity | `src/entity/` | 상수·선 합·선 ID |
| Control | `src/validate_lines.py` | 10선 오케스트레이션·status 결정 |
| Boundary | (미구현) | 입출력만 — Mom Test 범위 밖 |

### TDD

- RED → GREEN → REFACTOR; RED는 **`tests/`만** 수정
- assert 완화·skip·xfail 금지
- RED Command: `.cursor/commands/tdd-red.md`

### `.cursorrules` 점검 — 아직 문서에 없는 규칙 (후속 보완 후보)

- 10선 ↔ grid 인덱스·D1/D2 셀 좌표
- `MAGIC_CONSTANT` SSOT 및 리터럴 `34` 금지
- `incomplete` 시 `failed_lines=[]` 명시·status 우선순위
- RED 중 `src/` 전체·비-tests 파일 수정 금지 세부

---

## 5) 미완·다음 단계 체크리스트

- [ ] `.cursorrules` 빠진 규칙 반영 (SSOT·10선 좌표·incomplete·RED 세부)
- [ ] Test Loop 사이클 1 **RED** — SC-02 대각선 ( `/tdd-red` )
- [ ] GREEN — `src/` 최소 구현
- [ ] (선택) `tdd-green.md` · `tdd-refactor.md` Command
- [ ] `docs/PRD.md` · DESIGN (워크북 STEP 4)

---

## 6) 문서 추적성

```
03_세션3_워크북 (Rule·Command·Test Loop 정의)
  → 본 세션: Harness · .cursorrules · tdd-red · export-session
  → Prompt/04_세션3_인프라_구축_프롬프트.md (transcript)
  → (다음) Test Loop 사이클 1 RED — validate_lines
```
