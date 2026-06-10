# REFACTOR Safe — 통과 유지 구조 개선

ARRR **Review(R②)** 전용. `/refactor-smell` 블록 3 handoff 기준으로 **구조만** 개선한다.  
**동작·공개 API·테스트 assert는 변경하지 않는다.** 전체 `pytest` exit 0 유지.

## Phase 선언 (응답 첫 줄, 필수)

```
Phase: refactor | Layer: entity|control | Track: Logic | Target: validate_lines
```

- `Layer`: 이번 REFACTOR가 정리하는 ECB 계층
- 전제: `/refactor-smell` handoff 또는 동등한 냄새 목록이 채팅에 있음

## 입력 (추가 질문 없이 자동 추출)

사용자가 `/refactor-safe`만 호출해도 동작한다.

| 소스 | 추출 항목 |
|------|-----------|
| 직전 `/refactor-smell` 블록 3 | 수정 허용 파일·1회 범위·우선순위 |
| smell 없음 | S001/S002 기준 — Entity 분리 후보를 **최소 1건**만 |
| `src/`·`tests/` 현재 상태 | 추출·rename·move 대상 |
| `.cursorrules` | ECB·SRP·공개 API 고정 |

**추가 입력을 요구하지 말 것.** handoff 없으면 **가장 심각도 높은 냄새 1건**만 처리한다.

## 대상 계약 (변경 금지)

```python
validate_lines(grid) -> {
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": [...]   # pass·incomplete 시 []
}
```

- `src/validate_lines.py` — Control 진입점 **시그니처·반환 형식** 고정
- 10선·`MAGIC_CONSTANT`·`incomplete` 규칙 유지

## 안전 REFACTOR 절차

1. **범위 확정** — smell handoff의 **1~2건**만. 새 요구·다음 Test Loop 선행 금지.
2. **작은 단계** — extract → rename → move 순. 각 단계 후 pytest (또는 마지막에 1회).
3. **Entity 분리 우선** — 선 합·선 ID → `src/entity/` (예: `lines.py`, `grid.py`).
4. **Control 슬림화** — `validate_lines`는 10선 일괄 호출·status 결정만.
5. **테스트** — assert **변경 금지**. fixture 정리(conftest 이동)만 허용.
6. **회귀** — `python -m pytest tests/ -v` → exit 0.

## pytest

```bash
python -m pytest tests/ -v
```

REFACTOR 중 실패 시: 변경 **되돌리거나** `/green-minimal` 수준의 최소 수정으로 복구 — assert 완화 금지.

## 보고 형식 (REFACTOR 종료 시)

```markdown
## REFACTOR Safe 보고 — validate_lines

- Phase: refactor | Layer: … | Track: Logic | Target: validate_lines
- 처리 냄새: (예: S001 — Control 비만)
- 변경: (extract/rename/move 요약, 파일 경로)
- ECB: Entity … / Control … (1줄씩)
- pytest: `python -m pytest tests/ -v` → exit 0 ✓
- 다음: Test Loop 다음 사이클 — `/red-test-plan`
```

## 금지 (REFACTOR)

| 금지 | 이유 |
|------|------|
| `validate_lines` 시그니처·반환 키 변경 | 공개 API |
| `tests/` assert **완화·삭제** | 행위 변경 |
| RED·GREEN **새 요구** 구현 | 1사이클 = 1묶음 |
| `@pytest.mark.skip` / `xfail` | 우회 |
| Boundary(UI·CLI)·솔버·5×5·힌트 | Mom Test |
| smell handoff **3건 이상** 한 번에 | 범위 폭발 |

## 허용 예시

| 조치 | 허용 조건 |
|------|-----------|
| `def _sum_row(...)` → `entity/lines.py` | 동일 입력·출력, 테스트 불변 |
| `grid` fixture → `conftest.py` | assert 동일 |
| 리터럴 `34` → `MAGIC_CONSTANT` | 동작 동일 |
| private 함수 rename | 테스트가 import하지 않을 때 |

## Mom Test 게이트

구조 개선만. 증거 없는 기능·모듈 추가 금지.

## 완료 조건

- [ ] Phase 선언 첫 줄
- [ ] handoff 1~2건만 반영
- [ ] 공개 API·테스트 assert 불변
- [ ] `python -m pytest tests/ -v` exit 0

**완료 한 줄 (응답 마지막, 필수):**

```
Test Loop 다음 사이클 — /red-test-plan
```

## 다음 단계

1. `/export-session` — 사이클 마감 시 Report+Prompt 쌍 (선택)
2. `/red-test-plan` — Test Loop 다음 RED 묶음
