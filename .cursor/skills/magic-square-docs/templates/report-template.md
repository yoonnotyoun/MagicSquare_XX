# <제목> — MagicSquare_XX

**작성일:** YYYY-MM-DD
**근거:** (<이전 Report·워크북·`.cursorrules` 링크>)
**관련 프롬프트:** `Prompt/NN_<주제>_프롬프트.md`

---

## 1) 세션 목적

(이 세션에서 달성한 것 1~3문장)

---

## 2) 사용자 요청 요약

| # | 요청 | 결과 |
|---|------|------|
| 1 | | |

---

## 3) 산출물 목록

| 경로 | 역할 |
|------|------|
| | |

---

## 4) 주요 결정·계약

### 도메인·API

- 4×4, 빈 칸 `0`, 1~16, 마법상수 34, 10선 (R1~R4·C1~C4·D1·D2)
- `validate_lines(grid) -> { status, failed_lines }`

### ECB·TDD

| 항목 | 내용 |
|------|------|
| SC ID | (예: SC-02) |
| Test ID | (예: T-D1-01) |
| ARRR 단계 | (예: Record — `/red-skeleton` → `/tdd-red`) |
| pytest | (명령·exit code) |

---

## 5) 미완·다음 단계 체크리스트

- [ ] (다음 Command: `/…`)
- [ ] Test Loop 사이클 N+1

---

## 6) 문서 추적성

```
(선행 Report)
  → 본 Report
  → Prompt/NN_…_프롬프트.md
  → (다음) …
```
