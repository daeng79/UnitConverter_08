# Export Prompting — UnitConverter_08 세션 (워크북)

## 메타정보

| 항목 | 내용 |
|------|------|
| Prefix | `1` |
| Export 시각 | 2026-06-11 10:49 |
| 총 사용자 프롬프트 | 2개 |
| 선행 export | `prompting/0_export_prompting_2026-06-11_1048.md` (Mom Test·`/export` 구축) |

---

## 프롬프트 목록 (시간순)

### [1] 사용자 프롬프트

> 좋아.  지금까지 MOM TEST 한 인터뷰 내용을 기반으로 아래 내용을 만들어봐.
>
> Mom Test 결과:
> - 페르소나: [...]
> - 진짜 문제 (한 문장): [...]
> - Mom Test 증거 3줄: [...]
>
> 워크북을 채워줘:
> 1) 주제 한 문장 (Mom Test 기반, 솔루션 최소화)
> 2) R-G-I-O (Role/Goal/Input/Output)
> 3) 성공 기준 3개 (Mom Test 증거와 연결)
> 4) 표면 문제 — 이번 프로젝트에서 하지 않을 것
> 8계층 중 이번 세션에서 만드는 것만: Rule, Command, (Skill), Test Loop

**맥락/의도:** Mom Test 인터뷰 결과를 세션 워크북 형식으로 구조화 — 8계층 중 Rule/Command/Skill/Test Loop만 정의

---

### [2] 사용자 프롬프트

> /export

**맥락/의도:** `/export` 명령어 실행 — 현재 챗 세션(워크북 작성) report·prompting 파일 생성

---

## 재사용 가능한 프롬프트 패턴

### 패턴 1: Mom Test → 워크북 변환
```
좋아. 지금까지 MOM TEST 한 인터뷰 내용을 기반으로 아래 내용을 만들어봐.

Mom Test 결과:
- 페르소나: [...]
- 진짜 문제 (한 문장): [...]
- Mom Test 증거 3줄: [...]

워크북을 채워줘:
1) 주제 한 문장 (Mom Test 기반, 솔루션 최소화)
2) R-G-I-O (Role/Goal/Input/Output)
3) 성공 기준 3개 (Mom Test 증거와 연결)
4) 표면 문제 — 이번 프로젝트에서 하지 않을 것
8계층 중 이번 세션에서 만드는 것만: Rule, Command, (Skill), Test Loop
```
→ Mom Test 증거를 실행 가능한 Rule·Command·Test Loop로 전환

### 패턴 2: 세션 마감 export
```
/export
```
→ 챗 세션 요약·프롬프트를 `report/`, `prompting/`에 prefix 순차 저장

### 패턴 3: 워크북 + 후속 구현 연계 (확장)
```
워크북 SC-1~3 기준으로 `.cursor/commands/`에 Command 실파일 만들어줘
```
→ 워크북 초안을 Cursor 슬래시 명령어로 구체화 (후속 세션용)
