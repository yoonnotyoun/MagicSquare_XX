---
name: magic-square-docs
description: >-
  MagicSquare_XX 세션 문서를 Report·Prompt(transcript) 쌍과 TDD 체크리스트로
  생성한다. export-session, Report, Prompt, transcript, 세션 정리, ARRR 마감,
  Test Loop 체크리스트 요청 시 적용한다.
---

# MagicSquare_XX 문서 (Report · Prompt · Checklist)

세션·TDD 사이클 결과를 **추적 가능한 문서**로 남긴다.  
실행 트리거: `.cursor/commands/export-session.md` (전체 대화 export) 또는 본 Skill (템플릿·체크리스트).

## SSOT

| 문서 | 역할 |
|------|------|
| `.cursor/commands/export-session.md` | Report+Prompt 쌍 생성 절차·금지 |
| `.cursorrules` | 도메인·API·ECB·TDD |
| `docs/PRD.md` (있으면) | FR/NFR |
| `Report/`·`Prompt/` 기존 `NN_*` | 다음 번호 = **두 폴더 중 최대 NN + 1** |

## 언제 무엇을 쓸지

| 목적 | 사용 |
|------|------|
| 대화 전체 export | `/export-session` Command |
| Report/Prompt **형식만** 필요 | [templates/report-template.md](templates/report-template.md) · [templates/transcript-template.md](templates/transcript-template.md) |
| ARRR·Test Loop **마감 점검** | [templates/checklist-template.md](templates/checklist-template.md) |

## Report + Prompt 쌍 (export-session 규칙)

1. **항상 2개** — `Report/NN_<주제>_MagicSquare_XX.md` + `Prompt/NN_<주제>_프롬프트.md`
2. **동일 NN** — 두 폴더 중 더 큰 번호 + 1
3. **덮어쓰기 금지** — 기존 `NN_*` 수정하지 않고 신규 번호
4. **범위** — export 시 `Report/`·`Prompt/`·`.cursor/commands/` 외 **수정 금지** (export-session Command 따름)

### Phase 선언 (export 시)

```
Phase: export | Track: Documentation | Target: Report + Prompt
```

## Report 작성 요령

- 구현 코드 **본문 생략** — 경로·역할·결정만
- `.cursorrules`·Command·Skill 변경 있으면 §3·§4에 기록
- SC ID·Test ID·pytest 결과·다음 Command handoff 포함

## Prompt (transcript) 작성 요령

- Turn 순서 유지. 사용자 발화는 **가능하면 원문**
- Ask mode(파일 미변경) 턴도 기록
- 「재현 프롬프트」블록 — 동일 작업 재실행용

## TDD 체크리스트

ARRR 사이클 마감 시 [templates/checklist-template.md](templates/checklist-template.md)를 채워 Report §5 또는 별도 섹션에 붙인다.

## 금지

| 금지 | 이유 |
|------|------|
| Report만·Prompt만 단독 생성 (export-session 시) | replay 근거 상실 |
| 기존 NN 덮어쓰기 | 추적성 |
| transcript 없이 요약만 | Prompt가 SSOT |

## 템플릿

- [templates/report-template.md](templates/report-template.md)
- [templates/transcript-template.md](templates/transcript-template.md)
- [templates/checklist-template.md](templates/checklist-template.md)

## 관련 Command·Skill

- `/export-session` — 대화 export (본 Skill 템플릿과 형식 일치)
- `magic-square-tdd` — ARRR 사이클 진행 후 export 권장
