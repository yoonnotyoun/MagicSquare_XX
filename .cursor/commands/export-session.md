# Export Session — 대화 정리 내보내기

현재(또는 지정) 대화를 정리해 **Report** 보고서와 **Prompt** transcript를 **쌍으로** 생성한다.

## Phase 선언 (응답 첫 줄, 필수)

```
Phase: export | Track: Documentation | Target: Report + Prompt
```

## 번호 규칙

1. `Report/`·`Prompt/` 각각 `NN_`로 시작하는 파일 목록을 확인한다.
2. **두 폴더 중 더 큰 번호**를 찾아 **+1**을 다음 번호로 쓴다. (한쪽만 있으면 그쪽 기준)
3. 기본 형식: **2자리** (`04`, `05`, …). `9` 다음은 `10`.
4. Report와 Prompt는 **동일 번호**를 쓴다.

**현재 예:** `01`~`03` 존재 → 다음은 `04`.

## 생성 대상 (항상 2개)

| 폴더 | 파일 | 역할 |
|------|------|------|
| `Report/` | `NN_<주제>_MagicSquare_XX.md` | 세션 **결과 보고서** (산출물·결정·다음 단계) |
| `Prompt/` | `NN_<주제>_프롬프트.md` | **transcript export** (사용자 요청·에이전트 수행 기록) |

## Report 보고서 형식

```markdown
# <제목> — MagicSquare_XX

**작성일:** YYYY-MM-DD
**근거:** (이전 Report·워크북 링크)
**관련 프롬프트:** `Prompt/NN_…_프롬프트.md`

---

## 1) 세션 목적
## 2) 사용자 요청 요약 (표)
## 3) 산출물 목록 (경로·역할)
## 4) 주요 결정·계약 (도메인·API·ECB·TDD)
## 5) 미완·다음 단계 체크리스트
## 6) 문서 추적성
```

- 구현 코드 본문은 요약만. 경로와 역할 위주.
- `.cursorrules`·하네스·Command 변경이 있으면 반드시 기록.

## Prompt transcript 형식

```markdown
# <제목> — 프롬프트

**프로젝트:** MagicSquare_XX
**용도:** (이 세션 replay용 transcript)
**관련 보고서:** `Report/NN_…_MagicSquare_XX.md`

---

## 대화 transcript

### Turn N — 사용자
(요청 원문 또는 요약)

### Turn N — 에이전트
(수행 내용·생성/수정 파일·핵심 결정)

---

## 재현 프롬프트 (요약)
(동일 작업을 다시 시킬 때 붙여넣을 블록)

## 산출물 매핑
| 요청 | 결과 파일 |
```

- Turn 순서대로. 사용자 발화는 가능하면 원문 유지.
- Ask mode 등 **파일 미변경** 턴도 기록.

## 실행 절차

1. `Report/NN_*`, `Prompt/NN_*` 목록으로 다음 번호 결정.
2. 대화 전체를 훑어 Turn별 transcript 초안 작성.
3. Report 보고서 작성 (산출물·결정 중심).
4. Prompt transcript 작성 (대화 기록 중심).
5. **동일 NN**으로 두 파일 저장.
6. 응답 마지막에 생성 경로 2개를 명시.

## 금지

| 금지 | 이유 |
|------|------|
| 기존 `Report/NN_*`·`Prompt/NN_*` **덮어쓰기** | 번호는 항상 신규 |
| Report **또는** Prompt **하나만** 생성 | 쌍으로 보존 |
| `Report/`·`Prompt/`·`.cursor/commands/` **외** 파일 수정 | export는 문서만 |
| transcript 없이 Report만 요약 | Prompt가 replay 근거 |

## 완료 조건

- [ ] `Report/NN_…_MagicSquare_XX.md` 신규 생성
- [ ] `Prompt/NN_…_프롬프트.md` 신규 생성 (동일 NN)
- [ ] 번호 충돌 없음 (기존 최대+1)
- [ ] 다른 폴더 미수정
