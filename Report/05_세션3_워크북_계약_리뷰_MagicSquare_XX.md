# 세션 3 워크북 — validate_lines 계약 정합 리뷰 — MagicSquare_XX

**작성일:** 2026-06-10  
**근거:** [03_세션3_워크북_MagicSquare_XX.md](03_세션3_워크북_MagicSquare_XX.md) · [.cursorrules](../.cursorrules)  
**관련 프롬프트:** `Prompt/05_세션3_워크북_계약_리뷰_프롬프트.md`

---

## 1) 세션 목적

`03_세션3_워크북` §2 R-G-I-O·§3 성공 기준 3개(SC-01~03)가 **`validate_lines` 공개 API 계약**과 일치하는지 **리뷰만** 수행한다. 파일 수정 없음(Ask mode).

---

## 2) 사용자 요청 요약

| # | 요청 | 결과 |
|---|------|------|
| 1 | `03_세션3_워크북` R-G-I-O·SC-01~03 ↔ `validate_lines` 계약 대조 | 빠지거나 어긋난 항목만 표로 정리 |
| 2 | `/export-session` | 본 Report·Prompt `05`번 쌍 생성 |

---

## 3) 산출물 목록

| 경로 | 역할 |
|------|------|
| `Report/05_세션3_워크북_계약_리뷰_MagicSquare_XX.md` | 본 보고서 — 리뷰 결과·후속 권고 |
| `Prompt/05_세션3_워크북_계약_리뷰_프롬프트.md` | 대화 transcript |

**코드·규칙 파일 변경 없음** (리뷰 전용 세션).

---

## 4) 주요 결정·계약

### 리뷰 기준 (`validate_lines` 계약)

리뷰 시점에 워크북·`.cursorrules`·`src/validate_lines.py`를 대조. 계약 정본은 `.cursorrules` 공개 API:

```python
validate_lines(grid) -> {
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": [...]   # 예: ["R2", "D1"]; pass·incomplete 시 []
}
```

- **10선:** R1~R4, C1~C4, D1(주), D2(반) — 누락·한쪽만 검사 금지
- **빈 칸:** `0` → `incomplete` (완료 판정 불가)
- **Control 진입점:** `src/validate_lines.py`

### 정합한 핵심 (표 제외)

- 4×4·목표합 34·10선 검사·양쪽 대각선 필수
- Goal·Input·Output·R-02~R-03·SC-02 본문과 대체로 일치
- `.cursorrules`가 워크북 대비 **빈 칸·함수명·status·failed_lines** 공백을 보완함

### 빠지거나 어긋난 항목 (워크북 기준)

| 구분 | `validate_lines` 계약 기대 | 워크북 (§2 R-G-I-O / §3 SC) | 유형 |
|------|---------------------------|------------------------------|------|
| **함수명·레이어** | 단일 진입점 `validate_lines` (10선 일괄) | Test Loop는 `verify_all_lines`·`sum_diagonals` 분리, `validate_lines` 미기재 | 어긋남 |
| **SC-03 ↔ R-G-I-O** | 격자 변경 시 10선 **재검산** 호출 의무 | SC-03·R-04에만 있음. R-G-I-O Goal/Input/Output에 재호출 요건 없음 | 빠짐 |
| **빈 칸 처리** | `0` → `incomplete`, 합산 규칙 명시 | Input만 "빈 칸 2개 가능", R-01 "추후 PRD 확정" | 빠짐 (`.cursorrules`에서 보완됨) |
| **SC-01 범위** | 행4+열4+대각선2 = 10선 전부 필수 | SC-01 판정조건은 **대각선 2줄 포함**만 명시 | 빠짐 |
| **SC-02 ↔ 실패 보고** | 미통과 시 축 종류·인덱스(`failed_lines`) 반환 | SC-02는 "완료 불가"만 — 반환 요건은 Goal/R-03에만 있음 | 빠짐 |
| **Output 세부** | 복수 줄 실패 시 보고 방식·선 ID 형식 | "어느 축" 단수 표현, `failed_lines`·`incomplete` 미언급 | 빠짐 (`.cursorrules`에서 보완됨) |

### 해석

- SC-03은 `validate_lines` **단일 호출** 계약이 아니라 **변경 후 재호출 오케스트레이션**(`verify_after_change` 등)에 가깝다.
- 워크북 Test Loop의 `verify_all_lines` 명칭은 `.cursorrules`의 `validate_lines`와 **용어 불일치** — PRD·워크북 갱신 시 통일 권장.

---

## 5) 미완·다음 단계 체크리스트

- [ ] `03_세션3_워크북` §3 SC-01·SC-02 판정조건에 10선 전체·`failed_lines` 반환 반영
- [ ] 워크북 Test Loop 함수명을 `validate_lines`로 `.cursorrules`와 통일
- [ ] R-G-I-O Output에 `status`·`incomplete`·`failed_lines` 계약 요약 추가
- [ ] SC-03을 R-G-I-O Goal 또는 별도 오케스트레이션 항목으로 명시
- [ ] Test Loop 사이클 1 RED (`/tdd-red`) — SC-02 대각선

---

## 6) 문서 추적성

```
03_세션3_워크북 (R-G-I-O · SC-01~03)
  → 04_세션3_인프라_구축 (.cursorrules · validate_lines 스텁)
  → 본 세션: 워크북 ↔ validate_lines 계약 정합 리뷰 (파일 미변경)
  → Prompt/05_세션3_워크북_계약_리뷰_프롬프트.md
  → (다음) 워크북 보완 · Test Loop RED
```
