# Test Loop · ARRR 마감 체크리스트 — MagicSquare_XX

**사이클 #:** (예: 1)
**SC ID:** (예: SC-02)
**Test ID:** (예: T-D1-01)
**작성일:** YYYY-MM-DD

---

## ARRR 단계

| ARRR | Command | 완료 | 증거 |
|------|---------|------|------|
| **A**sk | `/red-test-plan` | [ ] | C2C 블록 1~4 |
| **R**ecord | `/red-skeleton` | [ ] | tests/ 골격 |
| **R**ecord | `/tdd-red` | [ ] | pytest exit ≠ 0 |
| **R**un | `/green-minimal` | [ ] | pytest exit 0 |
| **R**un | `/golden-master` | [ ] | golden pass (권장) |
| **R**eview | `/refactor-smell` | [ ] | S001~S010 표 |
| **R**eview | `/refactor-safe` | [ ] | pytest exit 0 |

---

## 계약·게이트

| 항목 | OK |
|------|-----|
| 10선 검산 (누락·한쪽만 금지) | [ ] |
| `status` / `failed_lines` 계약 준수 | [ ] |
| 1사이클 = 요구 1묶음 | [ ] |
| assert 완화·skip·xfail 없음 | [ ] |
| E001~E005 없음 | [ ] |
| Mom Test 게이트 (R-05) | [ ] |
| ECB — Entity/Control 분리 방향 | [ ] |

---

## pytest 기록

| 명령 | 결과 | exit |
|------|------|------|
| RED: `python -m pytest …::test_… -v` | FAILED | ≠ 0 |
| GREEN: `python -m pytest tests/ -v` | PASSED | 0 |
| REFACTOR 후: `python -m pytest tests/ -v` | PASSED | 0 |

---

## 다음

- [ ] Command: `/red-test-plan` (사이클 #+1)
- [ ] (선택) `/export-session`
