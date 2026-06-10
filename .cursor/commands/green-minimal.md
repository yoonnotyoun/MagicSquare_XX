# GREEN Minimal — 최소 구현

ARRR **Run(R②)** 전용. **직전 RED가 실패한 테스트 1묶음**만 통과시키는 **`src/` 최소** 구현.  
리팩터·golden master·구조 개선은 `/golden-master`·`/refactor-*` 범위.

## Phase 선언 (응답 첫 줄, 필수)

```
Phase: green | Layer: entity|control | Track: Logic | Target: validate_lines
```

- `Layer`: 이번 GREEN이 채우는 ECB 계층 (RED와 동일 사이클)
- `Target`: 항상 `validate_lines`

## 입력 (추가 질문 없이 자동 추출)

사용자가 `/green-minimal`만 호출해도 동작한다.

| 소스 | 추출 항목 |
|------|-----------|
| 직전 RED 보고·실패 pytest | 대상 테스트 경로·assert 기대값 |
| `tests/` 최근 추가 테스트 | Arrange grid·status·failed_lines 기대 |
| `.cursorrules` | 10선·status·incomplete·ECB |
| `docs/PRD.md` (있으면) | FR·SC ID |
| `src/validate_lines.py`·`src/entity/` | 현재 스텁·상수 SSOT |

**추가 입력을 요구하지 말 것.** RED 테스트가 불명확하면 `tests/test_validate_lines.py`에서 **가장 최근 추가·실패** 테스트 1개를 대상으로 한다.

## 대상 계약 (SSOT)

```python
validate_lines(grid) -> {
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": [...]   # pass·incomplete 시 []
}
```

- `pass`: 10선 합 `MAGIC_CONSTANT`, 빈 칸 없음
- `fail`: 빈 칸 없으나 합 ≠ 34인 선 → `failed_lines`에 선 ID
- `incomplete`: 빈 칸(`0`) 존재 → `failed_lines=[]`
- 상수: `src/entity/constants.py` (`MAGIC_CONSTANT`, `LINE_IDS` 등). 리터럴 `34` 지양

## 최소 구현 원칙

1. **이번 RED 1묶음만** 통과 — 다음 사이클 요구를 미리 구현하지 않는다.
2. **YAGNI** — 통과에 불필요한 Entity 분리·헬퍼·일반화 금지 (REFACTOR에서).
3. **ECB 방향** — Entity(선 합·선 ID)는 `src/entity/`로, Control(`validate_lines`)은 오케스트레이션만. Boundary는 범위 밖.
4. **시그니처 고정** — `validate_lines(grid) -> dict` 변경 금지.

## pytest

```bash
# 이번 사이클 테스트만 (RED와 동일 경로)
python -m pytest tests/test_validate_lines.py::<test_fn> -v

# 회귀 — 기존 통과 테스트 유지 확인
python -m pytest tests/ -v
```

**GREEN 완료 조건:** 대상 테스트 **PASSED**, 전체 `pytest` exit code = 0.

## 보고 형식 (GREEN 종료 시)

```markdown
## GREEN 보고 — validate_lines

- Phase: green | Layer: … | Track: Logic | Target: validate_lines
- SC/요구: (예: SC-02 — D1 fail)
- 수정 파일: `src/…` (경로·역할 1줄씩)
- 최소 구현 요약: (추가한 로직 2~3줄 설명)
- pytest: `python -m pytest … -v` → PASSED (exit 0) ✓
- 다음: `/golden-master` — pass 기준선 · `/refactor-smell` — 냄새 점검
```

## 금지 (GREEN)

| 금지 | 이유 |
|------|------|
| `tests/` assert·테스트 **완화·삭제** | RED 우회 |
| 다음 Test Loop 사이클 **선행** 구현 | 1사이클 = 1묶음 |
| REFACTOR성 대규모 추출·이름 변경 | `/refactor-safe` |
| Boundary(UI·CLI) 추가 | Mom Test 범위 밖 |
| 솔버·자동 채우기·5×5·힌트 | R-05 게이트 |
| `@pytest.mark.skip` / `xfail` | 우회 |

## Mom Test 게이트

SC-01~03·10선 검산·status·failed_lines와 직접 연결된 최소 코드만.

## 완료 조건

- [ ] Phase 선언 첫 줄
- [ ] `src/`만 수정 (필요 시 `src/entity/` 추가 — **이번 사이클 범위**)
- [ ] 대상 RED 테스트 PASSED + 전체 pytest exit 0
- [ ] `tests/` assert 미변경

**완료 한 줄 (응답 마지막, 필수):**

```
/golden-master 로 pass 기준선을 잡자
```

## 다음 단계

1. `/golden-master` — 유효 4×4 격자 pass 회귀 테스트 (선택·권장)
2. `/refactor-smell` — ECB·SRP 냄새 점검 (Ask)
3. `/refactor-safe` — 통과 유지 리팩터
