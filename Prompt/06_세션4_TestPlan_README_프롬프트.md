# 세션 4 — PRD Test Loop 테스트 플랜 · README 갱신 — 프롬프트

**프로젝트:** MagicSquare_XX  
**용도:** PRD §9 기반 Test Plan 작성·README 갱신 세션 replay용 transcript  
**관련 보고서:** `Report/06_세션4_TestPlan_README_MagicSquare_XX.md`

---

## 대화 transcript

### Turn 1 — 사용자

```
@PRD.md (176-194)
의 테스트 내용에 대한 테스트 플랜을 작성해서 README.md를 업데이트해줘.
```

(첨부: `docs/PRD.md` 176–194행 — Test Loop · Test ID 표, C2C Rule3, pytest 명령)

### Turn 1 — 에이전트

- `docs/PRD.md` §9·FR/NFR · `.cursor/commands/red-test-plan.md` · 기존 `README.md` · `tests/test_validate_lines.py` · `src/entity/constants.py` 확인
- PRD §9 Test Loop 8개에 맞춰 C2C 형식 테스트 플랜 작성
- `README.md` 갱신:
  - 기존 TDD(ARRR) 섹션 유지
  - **Test Plan (PRD §9)** 섹션 신규 추가
    - Loop 개요 표 (SC · FR · Layer · Test ID)
    - Loop #1~#6: FR 인용 · Given/When/Then · 예상 함수명 · Expected RED Failure · 픽스처/invariant
    - Loop #7: ECB·SRP REFACTOR 체크리스트
    - Loop #8: Mom Test 회귀 체크리스트
    - ECB·Mock 점검 (E001~E005)
    - 진행 상태 표 — Loop #1 **다음 RED**
    - golden master grid 예시 (Loop #6)
- `tests/` · `src/` **미변경** (문서·플랜만)

---

### Turn 2 — 사용자

```
/export-session
```

### Turn 2 — 에이전트

- `Report/`·`Prompt/` 기존 최대 번호 `05` 확인 → 다음 `06`
- `Report/06_세션3_TestPlan_README_MagicSquare_XX.md` 생성 *(이후 Turn 3에서 세션 4로 정정)*
- `Prompt/06_세션3_TestPlan_README_프롬프트.md` 생성 *(이후 Turn 3에서 세션 4로 정정)*

---

### Turn 3 — 사용자

```
세션 4야
```

### Turn 3 — 에이전트

- 본 세션을 **세션 4**로 정정
- 파일명 `06_세션3_*` → `06_세션4_*` 로 변경
- Report·Prompt 본문 세션 번호·상호 참조 갱신
- 문서 추적성: 세션 3 = 워크북·계약 리뷰(03~05), 세션 4 = Test Plan·README(06)

---

## 재현 프롬프트 (요약)

```
@docs/PRD.md (§9 Test Loop · Test ID, 176-194행)
PRD §9 Test Loop 8개에 대한 C2C 테스트 플랜(Given/When/Then, Test ID, FR 매핑)을 작성하고
README.md에 "Test Plan (PRD §9)" 섹션으로 반영해줘.
/red-test-plan 4블록 형식에 맞추되 README용으로 Loop #1~#8 전체를 포함.
tests/ · src/ 는 수정하지 말 것.

완료 후 /export-session — Report/Prompt 최대 NN+1 쌍 생성 (세션 4).
```

---

## 산출물 매핑

| Turn | 요청 | 결과 |
|------|------|------|
| 1 | PRD §9 테스트 플랜 + README 업데이트 | `README.md` — Test Plan 섹션 추가 |
| 2 | export-session | `Report/06_*`, `Prompt/06_*` |
| 3 | 세션 4 정정 | `06_세션4_TestPlan_README_*` 로 파일명·본문 갱신 |

---

## 다음 단계

- [ ] `/red-skeleton` — Loop #1 `T-D1-01` (`test_d1_sum_not_magic_constant_returns_fail`)
- [ ] `/tdd-red` — pytest RED 확인
- [ ] README 진행 상태 표 갱신 (Loop #1 완료 시)
