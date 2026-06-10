# REFACTOR Smell — ECB·SRP 냄새 점검 (Ask)

ARRR **Review(R①)** 전용. **코드·테스트 냄새 목록만** 채팅에 출력한다.  
`src/`·`tests/` **파일 생성·수정 금지**. 수정은 `/refactor-safe`에서 한다.

## Phase 선언 (응답 첫 줄, 필수)

```
Phase: refactor | Layer: entity|control|boundary | Track: Logic | Target: validate_lines
```

- `Layer`: 점검 초점 계층 (복수면 `entity|control` 형태)
- 전제: 직전 GREEN·golden master로 **pytest exit 0**

## 입력 (추가 질문 없이 자동 추출)

사용자가 `/refactor-smell`만 호출해도 동작한다.

| 소스 | 추출 항목 |
|------|-----------|
| `src/validate_lines.py`·`src/entity/` | Control/Entity 책임·중복·결합 |
| `tests/` | AAA 구조·fixture·E001~E005 위반 |
| `.cursorrules` | ECB·SRP·Mom Test·10선 계약 |
| `docs/PRD.md` (있으면) | NFR·구조 요건 |
| 직전 GREEN·golden 보고 | 이번 사이클 변경 범위 |

**추가 입력을 요구하지 말 것.** 파일이 스텁만이면 **예상 냄새·REFACTOR 후보**를 SSOT 기준으로 제시한다.

## 점검 카탈로그 (MagicSquare_XX)

| ID | 냄새 | ECB/SRP 신호 | 심각도 |
|----|------|--------------|--------|
| S001 | **Control 비만** | `validate_lines`에 선 합·선 ID 계산이 직접 있음 | 높음 |
| S002 | **Entity 누락** | 10선 로직이 Control 한 함수에만 존재 | 높음 |
| S003 | **Boundary 침범** | (미래) 입출력 계층에 검산·status 결정 | 높음 |
| S004 | **Magic number** | 리터럴 `34`·`4` — `constants.py` SSOT 미사용 | 중간 |
| S005 | **10선 불완전** | 행/열만·대각선 한쪽만 검사 코드 경로 | 높음 |
| S006 | **status 혼선** | `incomplete`/`fail`/`pass` 우선순위·`failed_lines` 규칙 불명확 | 높음 |
| S007 | **테스트 결합** | 테스트가 내부 private 헬퍼·구현 세부에 고정 | 중간 |
| S008 | **Fixture 산재** | 동일 grid가 파일마다 복붙 | 낮음 |
| S009 | **E001~E005** | mock·skip·한쪽 축만 assert 등 (아래 표) | 높음 |
| S010 | **YAGNI 역전** | 다음 Test Loop 사이클 기능이 이미 구현됨 | 중간 |

**E001~E005 — 테스트 냄새**

| 코드 | 패턴 |
|------|------|
| E001 | Entity·도메인을 mock/patch |
| E002 | `validate_lines` 통과 위장 mock |
| E003 | 10선 중 일부만 assert |
| E004 | Boundary 테스트에 검산 로직 |
| E005 | skip·xfail·assert 완화 |

## 출력 형식 (3블록, 표 필수)

### 블록 1 — 냄새 목록

| ID | 위치 (파일·함수) | 냄새 | 심각도 | 근거 (1줄) |
|----|------------------|------|--------|------------|
| | | | 높음/중간/낮음 | |

(냄새 없으면 「현재 사이클 범위에서 S001~S010 해당 없음」 1행)

### 블록 2 — REFACTOR 제안 (우선순위)

| 순위 | 대상 | 제안 조치 | 기대 ECB 효과 | 리스크 |
|------|------|-----------|---------------|--------|
| 1 | | (예: `sum_line` → `entity/lines.py`) | Entity 분리 | 낮음 — 테스트 동작 동일 |

### 블록 3 — `/refactor-safe` handoff

| 항목 | 내용 |
|------|------|
| **수정 허용 파일** | `src/` (및 필요 시 `tests/conftest.py` fixture 정리만) |
| **금지** | assert 완화·public API 변경·Mom Test 밖 기능 |
| **회귀 명령** | `python -m pytest tests/ -v` |
| **1회 REFACTOR 범위** | 제안 **1~2건** (1사이클 = 1묶음) |

## 금지 (Ask = Review ①)

| 금지 | 이유 |
|------|------|
| `src/`·`tests/` **파일 수정** | `/refactor-safe` 범위 |
| RED·GREEN 재실행·새 기능 테스트 추가 | Phase가 refactor·Ask |
| Mom Test 밖 구조 (솔버·UI·5×5) 제안 | R-05 |
| 냄새 없는데 대규모 재설계 권고 | YAGNI |

## Mom Test 게이트

냄새·제안은 SC-01~03·10선·`validate_lines` 계약·ECB와 연결된 것만.

## 완료 조건

- [ ] Phase 선언 첫 줄
- [ ] 블록 1~3 표 **전부** 작성
- [ ] `/refactor-safe`에 바로 넘길 수 있는 우선순위·범위 명시
- [ ] `src/`·`tests/` 미변경

**완료 한 줄 (응답 마지막, 필수):**

```
/refactor-safe 로 REFACTOR 진행하자
```

## 다음 단계

1. `/refactor-safe` — 제안 1~2건 적용, pytest exit 0 유지
2. Test Loop **다음 사이클** — `/red-test-plan`
