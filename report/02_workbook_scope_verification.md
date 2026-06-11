# 세션 워크북 — UnitConverter 범위·검증 계약

## 메타정보

| 항목 | 내용 |
|------|------|
| 프로젝트 | UnitConverter_09 |
| 선행 export | `report/1_export_report_2026-06-11_1049.md` |
| 보완 | RGIO·SC·Rule·Test Loop — `UnitConverter.py` 계약 대조 리뷰 반영 |
| 목표 | 코드 손대기 **전** 범위·“맞다” 기준 고정 (구현 아님) |

---

## Mom Test 결과 (요약)

### 페르소나

6시간 실습 **UnitConverter** 개발자. README가 전체 스펙처럼 느껴지지만 실제 코드는 36줄 프로토타입. **“일단 돌아가게”**를 우선하고, 데모가 되면 범위 확인을 미루는 패턴.

### 진짜 문제 (한 문장)

**프로토타입이 동작한다는 이유로 README와 코드 사이의 범위·출력·확장 gap을 PM과 맞추지 않은 채 “중간 산출물”이라고 스스로 단정해, 코드를 손댈 때마다 전면 재작성과 결정 대기가 구현보다 먼저 발생하고 작업이 멈춘다.**

### Mom Test 증거 3줄

1. `main upload` 직후 README 재독 → **“프로토타입 구조로 추가 요구 3개를 붙일 수 없다”** 판단 → **사실상 다음 작업이 전면 재작성**
2. README–코드 gap을 알고도 **PM에게 물어보지 않음** → 답 0분, `spec` 브랜치만 따고 **확인을 미룸**
3. 변환 로직 검증을 **테스트 없이 5~7회 수동 실행**만 하고 끝 → **음수·반올림·교차 변환은 미검증** 상태로 멈춤

---

## 1) 주제 한 문장

> **UnitConverter에서 코드를 손대기 전에 README와 프로토타입 사이의 범위·“맞다”의 기준을 고정하여, 재작성과 수동 확인에만 쓰이는 시간을 차단한다.**

| 포함 | 제외 |
|------|------|
| 범위 in/out 확정, 검증 기준, Test Loop RED | OCP 리팩토링, 동적 등록, JSON/CSV 출력 |

---

## 2) R-G-I-O

| | 내용 |
|---|------|
| **Role** | UnitConverter 6시간 실습 **개발자** — 36줄 프로토타입 작성 후 README gap 인지·작업 중단 상태 |
| **Goal** | 코드 손대기 **전에** 범위·검증 기준을 고정해 **“수동 5번 → 전면 재작성”** 패턴을 차단한다 |
| **Input** | README + 현재 `UnitConverter.py` + Mom Test 증거 3줄 + 아래 **코드 계약 baseline** + PM 미결 3건 |
| **Output** | **범위 확정표**(in/out) + **검증 기준 3줄** + Rule·Command·Test Loop RED 초안 — “돌아간다”만으로 완료 단정 금지 |

### Input — 코드 계약 baseline (`UnitConverter.py` 현재 동작)

| 항목 | README 요구 | 코드 현재 (`UnitConverter.py`) | gap |
|------|------------|-------------------------------|-----|
| **입력 포맷** | `단위:값` (예: `meter:2.5`) | `unit:value` — 콜론 구분, 프롬프트 입력 | 일치 |
| **지원 단위** | meter, feet, yard | meter, feet, yard | 일치 |
| **변환 비율** | `1m=3.28084ft`, `1m=1.09361yd`, meter 경유 | 동일 상수·meter 중간값 | 일치 |
| **출력 줄 수** | 예시 2줄 (feet, yard) | **3줄** (meter·feet·yard 모두, 입력 단위 포함) | **불일치** |
| **출력 반올림** | 예시 `8.2`, `2.7` (소수 1자리로 추정) | **반올림 없음** (전체 float) | **불일치** |
| **입력 검증 — 형식** | 잘못된 형식 거부 | `:` 없으면 에러 메시지 후 return | 구현됨 |
| **입력 검증 — 숫자** | (명시 없음) | `float` 파싱 실패 시 에러 | 구현됨 |
| **입력 검증 — 미지원 단위** | 없는 단위 거부 | `Unknown unit` 에러 | 구현됨 |
| **입력 검증 — 음수** | 음수 검증 요구 | **검증 없음** (음수 허용) | **불일치** |
| **테스트** | 단위 변환·입력 검증 TC | **0건** | 미구현 |
| **설계·추가 요구** | OCP/SRP, 설정 외부화, 동적 등록, 출력 포맷 | 미구현 | 후속/범위 외 |

### Input — PM 미결 3건 (이번 마일스톤)

1. 이번 in/out — 기본 3단위+TC vs 추가 요구 3개
2. 출력 반올림 규칙 (`8.2 feet` vs 전체 소수) **및 출력 줄 수**(2줄 vs 3줄·동일 단위 포함 여부)
3. 음수 입력 처리 (에러 vs 허용)

---

## 3) 성공 기준 3개

| # | 성공 기준 | 연결 Mom Test 증거 |
|---|----------|-------------------|
| **SC-1** | 코드 작업 전 **이번 마일스톤 in/out**이 문서화되어 있다. **현재 코드 baseline**(위 표)이 in/out 표에 **“이미 있음 / gap / 범위 외”**로 명시되어 있다 | ② gap 인지 후 PM 미질문 → **범위 미정으로 작업 중단** |
| **SC-2** | 변환 “맞다” 기준이 **고정 문장**으로 문서화되어 있다 — 아래 **기준 5항** 중 PM 미결 항목은 `[미결]` 표시 | ① README 재독 후 **구조 충돌 인지·재작성 대기** |
| **SC-3** | 변환·입력·출력 계약 변경 시 **pytest RED ≥6**이 먼저 있고, 수동 실행은 **데모 1~2회만** | ③ **5~7회 수동만** 하고 음수·반올림·교차·형식 미검증 |

### SC-1 — in/out 표 (초안)

| 구분 | 항목 | 상태 |
|------|------|------|
| **IN (현재 baseline)** | `unit:value` 입력, meter/feet/yard 변환 | **있음** |
| **IN (현재 baseline)** | 형식·숫자·미지원 단위 에러 처리 | **있음** |
| **IN (gap → 이번 마일스톤)** | 음수 정책 | **미결** |
| **IN (gap → 이번 마일스톤)** | 출력 반올림·줄 수(README vs 코드) | **미결** |
| **IN (gap → 이번 마일스톤)** | pytest (변환·입력·출력) | **없음** |
| **OUT (후속/범위 외)** | OCP/SRP 리팩토링, 설정 외부화, 동적 등록, JSON/CSV | **범위 외** |

### SC-2 — “맞다” 기준 5항 (3줄 → 계약 보완)

| # | 기준 | 상태 |
|---|------|------|
| 1 | **meter 기준** — 모든 변환은 meter 중간값 경유 | 확정 (코드·README 일치) |
| 2 | **README 비율** — `1 meter = 3.28084 feet`, `1 meter = 1.09361 yard` | 확정 |
| 3 | **출력 반올림** — 소수 자릿수·반올림 방식 | **[미결]** PM |
| 4 | **출력 형태** — 줄 수(2 vs 3), 입력 단위 줄 포함 여부, README 예시와의 정합 | **[미결]** PM |
| 5 | **입력 검증** — 형식/미지원 단위: 에러; 음수: 에러 vs 허용 | 형식·단위 **확정(에러)**; 음수 **[미결]** PM |

---

## 4) 표면 문제 — 이번 프로젝트에서 하지 않을 것

| 표면 문제 (금지) | 왜 하지 않는가 |
|-----------------|---------------|
| **OCP/SRP 전면 리팩토링** | pain은 **범위·기준 미정**으로 손을 못 댐 |
| **설정 외부화 (JSON/YAML)** | **“언제·어디까지”** 미결 |
| **동적 단위 등록 (`cubit`)** | UX·저장 방식 미정 |
| **JSON/CSV/표 출력 포맷** | 반올림·줄 수 미확정 |
| **“데모 돌아가면 OK”로 범위 단정** | gap 인지 후 **확인 0분·spec으로 미룸** |
| **CI/CD·인프라 구축** | 이번 세션은 **판단·검증 계약** 고정 |

---

## 8계층 — Rule / Command / Skill / Test Loop

### Rule (보완)

```yaml
# unit-converter-scope-rules
rules:
  - id: SCOPE_BEFORE_CODE
    when: milestone_scope OR output_rule OR negative_policy is UNDEFINED
    then: no_implementation — document in/out only

  - id: TEST_BEFORE_MANUAL
    when: conversion_logic OR input_validation OR output_format changes
    then: pytest_RED_first — manual_demo_max_2

  - id: README_AS_VERIFICATION_SSOT
    baseline:
      - "1 meter = 3.28084 feet"
      - "1 meter = 1.09361 yard"
      - "feet/yard는 meter 기준 계산"
      - "입력 포맷: unit:value (콜론 구분)"
      - "출력 형태·반올림: PM 미결 — README 예시(2줄·1자리) vs 코드(3줄·raw float) gap 명시 필수"
      - "입력 검증: 형식/미지원 단위=에러(구현됨), 음수=PM 미결"

  - id: NO_GAP_DEFERRAL
    when: readme_code_gap_detected
    then: pm_scope_check_required — max_15min

  - id: MOM_TEST_ALIGNMENT
    evidence: [full_rewrite_wait, pm_zero_confirm, manual_5_7_unverified]
    success_criteria: [SC-1, SC-2, SC-3]
```

### Command

| Command | 목적 | Mom Test 연결 |
|---------|------|---------------|
| `/scope-check` | README vs 코드 gap → in/out 표(**baseline 포함**) | SC-1, 증거 ② |
| `/verify-baseline` | “맞다” **기준 5항** 확정 (반올림·출력 형태·음수) | SC-2, 증거 ① |
| `/test-plan-conversion` | 변환·입력·출력 **RED 테스트 목록** (≥6) | SC-3, 증거 ③ |
| `/mom-alignment` | Rule·Test Loop ↔ Mom Test·SC traceability | 전체 |

### Skill (선택)

```markdown
# unit-converter-spec

## Steps
1. `/scope-check` — in/out 표 + 코드 baseline gap 표
2. `/verify-baseline` — 기준 5항 + PM 미결 3건
3. `/test-plan-conversion` — RED ≥6 (변환·역변환·형식·단위·음수·출력 형태)
4. `/mom-alignment` — SC-1~3 traceability
```

### Test Loop — RED (보완: 3 → 6)

| # | RED 테스트 | 검증 대상 | Mom Test |
|---|-----------|----------|----------|
| R1 | `meter:2.5` → feet/yard 기대값 (**반올림 규칙 포함**) | 변환·반올림 gap | 증거 ③ |
| R2 | `feet:3.28084` → meter ≈ 1, feet→yard **meter 경유** 일치 | 역·교차 변환 | 증거 ③ |
| R3 | `meter:-2.5` → 음수 정책(에러/허용) 기대 동작 | 음수 미검증 | 증거 ③ |
| R4 | `invalid` (콜론 없음) → 형식 에러 메시지 | 입력 검증 — 형식 | 증거 ③ |
| R5 | `cubit:1` → 미지원 단위 에러 | 입력 검증 — 단위 | 증거 ③ |
| R6 | `meter:2.5` → **출력 줄 수·포함 단위·포맷** (README 2줄 vs 코드 3줄) | 출력 형태 gap | 증거 ③ |

| 단계 | 내용 |
|------|------|
| **GREEN** | (후속) 최소 구현 → RED 1개씩 통과 |
| **REFACTOR** | (후속) 변환·출력·입력 분리 — 단위 추가 시 3곳 수정 방지 (증거 ①) |

---

## 체크리스트

- [x] RGIO — 코드 계약 baseline 표 추가
- [x] SC-1 — in/out + baseline 상태 명시
- [x] SC-2 — “맞다” 기준 5항 (출력 형태·입력 검증 포함)
- [x] SC-3 / Test Loop — RED 6개 (형식·미지원 단위·출력 형태 추가)
- [x] Rule `README_AS_VERIFICATION_SSOT` — 입력 포맷·출력·검증 baseline 보완
