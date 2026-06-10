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

**다음 작업:** Test Loop #1 — SC-02 대각선 (`T-D1-01`) · [PRD §9](docs/PRD.md#9-test-loop--test-id)

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

```
Mom Test → 워크북 → .cursorrules → PRD → TDD(ARRR) → src/ · tests/
```
