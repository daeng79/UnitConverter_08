# Export Prompting — UnitConverter_09 세션 (문서·Command)

## 메타정보

| 항목 | 내용 |
|------|------|
| Prefix | `2` |
| Export 시각 | 2026-06-11 13:05 |
| 총 사용자 프롬프트 | 8개 |
| 선행 export | `prompting/1_export_prompting_2026-06-11_1049.md` (워크북) |

---

## 프롬프트 목록 (시간순)

### [1] 사용자 프롬프트

> @c:\DEV\UnitConverter_09\ 프로젝트에서 지금까지 진행한 내용을 바탕으로 루트 폴더 밑에 doc/PRD.md 문서를 만들어줘

**맥락/의도:** Mom Test·워크북·코드·테스트 상태를 종합한 PRD 초안 작성

---

### [2] 사용자 프롬프트

> @doc/PRD.md 바탕으로 @README.md 파일을 업데이트해라

**맥락/의도:** PRD와 정합된 README — M1/M2·TDD·현재 진행 상태 반영

---

### [3] 사용자 프롬프트

> .cursor/commands/red-test-plan.md Command 파일을 만들어줘.
> 참고 SSOT:
> - @.cursorrules
> - @docs/PRD.md
> - 기존 @.cursor/commands/tdd-red.md 형식
> 역할: ARRR A단계(Ask=RED ③) — C2C 설계표·테스트 플랜만 작성. tests/·src/ 파일 생성 금지.
> (… Phase 선언, 4블록 출력, ECB·Mock, 완료 한 줄 등 상세 지시 …)

**맥락/의도:** RED ③ 테스트 플랜 전용 슬래시 명령어 — 파일 수정 없이 C2C·Track B·플랜 4블록

---

### [4] 사용자 프롬프트

> 요청 내용 중 - 상수 34/16/4는 entity/constants.py import (픽스처 데이터만) 부분은 잘못된 요청이었다. @c:\DEV\UnitConverter_09\ 에 맞게 red-skeleton 을 다시 수정해줘.

**맥락/의도:** red-skeleton에서 Grid/entity 범용 템플릿 제거 · UnitConverter_09 전용으로 재작성

---

### [5] 사용자 프롬프트

> .cursor/commands/green-minimal.md Command 파일을 만들어줘.
> 역할: ARRR R단계(Respond=GREEN) — RED 1묶음당 최소 구현, 1커밋=1 RED 묶음.
> (… Phase, 절차, constants.py, ECB, 금지, 보고, pytest 예시 …)

**맥락/의도:** GREEN 최소 구현 Command — src/constants SSOT · 1 RED = 1 commit 원칙

---

### [6] 사용자 프롬프트

> .cursor/commands/golden-master.md Command 파일을 만들어줘.
> 역할: GREEN PASS 후 Golden Master(Approval Test) 구축·검증.
> (… assert_matches_golden, UPDATE_GOLDEN, int[6] 1-index, 에러 포맷, 보고 …)

**맥락/의도:** Approval Test · golden 파일 재생성 규칙 · 수동 편집 금지

---

### [7] 사용자 프롬프트

> .cursor/commands/refactor-smell.md Command 파일을 만들어줘.
> 역할: ARRR R단계(Refine ⑦) — 코드 스멜 탐지만, 수정·commit 금지.
> (… pytest PASS 전제, P0/P1/P2, Change Budget, /refactor-safe 후보 …)

**맥락/의도:** Refine ⑦ 스멜 탐지 전용 — 수정 없이 표 + safe 후보 1~3개

---

### [8] 사용자 프롬프트

> /export

**맥락/의도:** 본 세션 report·prompting export (prefix 2)

---

## 재사용 가능한 프롬프트 패턴

### 패턴 1: PRD → README 정합

```
@doc/PRD.md 바탕으로 @README.md 파일을 업데이트해라
```

→ SSOT PRD를 진입용 README로 요약·링크

### 패턴 2: ARRR Command 생성 (SSOT + 기존 형식)

```
.cursor/commands/{name}.md Command 파일을 만들어줘.
참고 SSOT: @.cursorrules, @doc/PRD.md, @.cursor/commands/{기존}.md
역할: ARRR {단계} — {한 줄 역할}. {수정 허용/금지}.
본문 포함: Phase 선언, 절차, 금지, 보고, 완료 한 줄
```

→ TDD·ARRR 파이프라인 슬래시 명령어 표준화

### 패턴 3: Command 보정 (프로젝트 맞춤)

```
요청 내용 중 {잘못된 부분}은 잘못된 요청이었다. @{프로젝트}에 맞게 {command}를 다시 수정해줘.
```

→ 타 프로젝트 템플릿 잔재 제거

### 패턴 4: 세션 마감 export

```
/export
```

→ `report/`, `prompting/` prefix 순차 저장
