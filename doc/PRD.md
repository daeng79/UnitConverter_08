# PRD — UnitConverter_08

| 항목 | 내용 |
|------|------|
| 문서 버전 | 1.0 |
| 작성일 | 2026-06-11 |
| 프로젝트 | UnitConverter_08 — 길이 단위 변환 CLI |
| 상태 | 범위·검증 계약 고정 완료, TDD RED 진행 중 (R1 1건 작성) |

---

## 1. 배경

UnitConverter_08는 6시간 실습용 **길이 단위 변환 CLI** 프로젝트이다. README에는 OCP/SRP 설계, 설정 외부화, 동적 단위 등록, 다양한 출력 포맷 등 광범위한 요구사항이 명시되어 있으나, 초기 업로드 시점의 `UnitConverter.py`는 **36줄 절차형 프로토타입**에 그쳤다.

Mom Test 인터뷰(2026-06-11) 결과, 핵심 문제는 기능 부재가 아니라 **README와 코드 사이의 범위·“맞다” 기준이 PM과 확정되지 않은 채 구현을 시도**하여, 재작성·결정 대기·수동 검증에 시간이 소모된다는 점이었다.

본 PRD는 Mom Test, 세션 워크북(`report/02_workbook_scope_verification.md`), `.cursorrules`, 현재 코드·테스트 상태를 종합하여 **이번 마일스톤의 제품 요구사항**을 정의한다.

---

## 2. 문제 정의 (Mom Test)

### 페르소나

6시간 실습 UnitConverter 개발자. README를 전체 스펙처럼 인식하지만 실제 코드는 프로토타입 수준. **“일단 돌아가게”**를 우선하고, 데모가 되면 범위 확인을 미루는 패턴.

### 진짜 문제 (한 문장)

> 프로토타입이 동작한다는 이유로 README와 코드 사이의 범위·출력·확장 gap을 PM과 맞추지 않은 채 “중간 산출물”이라고 스스로 단정해, 코드를 손댈 때마다 전면 재작성과 결정 대기가 구현보다 먼저 발생하고 작업이 멈춘다.

### 증거

| # | 증거 | 영향 |
|---|------|------|
| 1 | README 재독 후 추가 요구 3개를 프로토타입 구조로 붙일 수 없다고 판단 → **전면 재작성 대기** | SC-2, REFACTOR 필요성 |
| 2 | README–코드 gap을 알고도 **PM에게 물어보지 않음** → 답 0분, spec 브랜치만 따고 확인 미룸 | SC-1, 범위 미정 |
| 3 | 변환 로직을 **테스트 없이 5~7회 수동 실행**만 하고 끝 → 음수·반올림·교차 변환 미검증 | SC-3, pytest 선행 |

---

## 3. 목표

### 제품 목표

사용자가 `단위:값` 형식으로 길이를 입력하면, meter / feet / yard 세 단위로 변환 결과를 출력하는 CLI를 제공한다.

### 프로세스 목표 (이번 마일스톤)

코드를 손대기 **전에** 범위·검증 기준을 고정하고, **pytest RED → GREEN → REFACTOR** 순서로 구현하여 “수동 5번 → 전면 재작성” 패턴을 차단한다.

### 성공 조건 (SC-1 ~ SC-3)

| SC | 조건 | 완료 판정 |
|----|------|----------|
| **SC-1** | 마일스톤 in/out 문서화. baseline 항목마다 **있음 / gap / 범위 외** 표시 | in/out 표 존재 + PM 미결 항목 `[미결]` 명시 |
| **SC-2** | 변환 “맞다” 기준 **5항** 고정 문서화 | 확정 항목은 기대값·에러 계약과 일치 |
| **SC-3** | 계약 변경 전 pytest **RED ≥6** 선행. 수동은 **데모 1~2회** | R1~R6 각 1 test, GREEN 후 전체 PASS |

상세 traceability → `report/02_workbook_scope_verification.md`

---

## 4. 범위

### 4.1 IN — 이번 마일스톤 포함

| 항목 | 상태 | 설명 |
|------|------|------|
| 입력 포맷 `unit:value` | **있음** | 콜론 1개로 단위·값 구분 (예: `meter:2.5`) |
| 지원 단위 meter / feet / yard | **있음** | 세 단위 간 변환 |
| 변환 비율 (meter 기준) | **확정** | 아래 §5 참조 |
| 형식·숫자·미지원 단위 에러 처리 | **있음** | `ValueError` (메시지 포함) |
| 순수 변환 로직 모듈 | **진행 중** | `src/unit_converter.py` (현재 stub) |
| pytest 테스트 | **진행 중** | RED R1 1건 작성, R2~R6 미작성 |
| TDD 워크플로 | **확정** | RED → GREEN → REFACTOR, `.cursor/commands/tdd-red.md` |

### 4.2 IN — gap (PM 확정 필요)

| 항목 | 상태 | README vs 코드 gap |
|------|------|-------------------|
| **출력 반올림** | **[미결] PM** | README 예시 `8.2`, `2.7` (소수 1자리 추정) vs 코드 raw float |
| **출력 줄 수·형태** | **[미결] PM** | README 2줄 (feet, yard) vs 코드 3줄 (meter·feet·yard 모두) |
| **음수 입력 정책** | **[미결] PM** | README “음수 검증” vs 코드 음수 허용 |

PM 미결 항목은 RED 테스트에 `# [미결: PM]` 주석과 명시적 기대값으로 기록하며, **확정 전 `src/` 구현 추측 금지**.

### 4.3 OUT — 이번 마일스톤 제외 (후속)

| 항목 | 사유 |
|------|------|
| OCP/SRP 전면 리팩토링 | pain은 범위·기준 미정; REFACTOR 단계에서 최소 개선만 |
| 설정 외부화 (JSON/YAML) | “언제·어디까지” 미결 |
| 동적 단위 등록 (`cubit` 등) | UX·저장 방식 미정 |
| JSON / CSV / 표 출력 포맷 | 반올림·줄 수 미확정 |
| CI/CD·인프라 구축 | 이번 세션은 판단·검증 계약 고정 |
| “데모 돌아가면 OK”로 범위 단정 | Mom Test 증거 ②·③와 충돌 |

README의 추가 요구사항 3개(설정 외부화, 동적 등록, 출력 포맷 선택)는 **후속 마일스톤(M2)** 으로 분리한다.

---

## 5. 비즈니스 규칙 (확정)

### 변환 상수

| 상수 | 값 |
|------|-----|
| `METER_TO_FEET` | `3.28084` |
| `METER_TO_YARD` | `1.09361` |

### 변환 원칙

1. **모든 변환은 meter 중간값을 경유**한다.
2. feet ↔ yard 간 비율도 meter 기준으로 계산한다.
3. README 예시: `meter:2.5` → `8.2 feet`, `2.7 yard` (반올림 규칙은 §4.2 미결).

### 입력 검증 (확정 부분)

| 조건 | 동작 |
|------|------|
| 콜론(`:`) 없음 | `ValueError` — 형식 오류 |
| 숫자 파싱 실패 | `ValueError` — 숫자 오류 |
| 미지원 단위 (예: `cubit`) | `ValueError` — 미지원 단위 |
| 음수 값 | **[미결] PM** — 에러 vs 허용 |

---

## 6. 기능 요구사항

### FR-1. 입력 파싱

- **형식**: `unit:value` (콜론 1개)
- **예시**: `meter:2.5`, `feet:3.28084`, `yard:1.09361`
- **API**: `parse_input(input_str: str) -> tuple[str, float]`

### FR-2. 단위 → meter 환산

- 지원 단위: `meter`, `feet`, `yard`
- **API**: `to_meters(unit: str, value: float) -> float`

### FR-3. 전 단위 변환

- 입력 단위·값을 받아 세 단위 모두로 변환
- 반환 dict 키: `{"meter", "feet", "yard"}`
- **API**: `convert_all(unit: str, value: float) -> dict[str, float]`

### FR-4. 출력 포맷

- 변환 결과를 CLI 출력용 문자열 목록으로 반환
- 줄 수·반올림·입력 단위 포함 여부 → **[미결] PM** (README 2줄 vs baseline 3줄)
- **API**: `format_output(unit: str, value: float, converted: dict[str, float]) -> list[str]`

### FR-5. CLI (후속 연동)

- 진입점: `UnitConverter.py` (현재 baseline, 36줄)
- `src/unit_converter.py` 구현 완료 후 CLI 연동
- 현재 baseline 동작:
  - 프롬프트 입력 → 파싱 → 3줄 출력 (meter·feet·yard, raw float)
  - 형식·숫자·미지원 단위는 print 후 return (dict status API 미사용)

---

## 7. API 계약 (`src/unit_converter.py`)

```
parse_input(input_str: str) -> tuple[str, float]
    # "unit:value" 파싱. 형식·숫자·미지원 단위 오류 시 ValueError.

to_meters(unit: str, value: float) -> float
    # 입력 단위·값 → meter 환산값.

convert_all(unit: str, value: float) -> dict[str, float]
    # {"meter": float, "feet": float, "yard": float}

format_output(unit: str, value: float, converted: dict[str, float]) -> list[str]
    # 출력 줄 목록. 반올림·줄 수는 PM 미결 — RED 테스트가 SSOT.
```

**현재 구현 상태**: 4개 함수 모두 stub (`...`만 존재).

---

## 8. README vs 코드 baseline 대조

| 항목 | README | `UnitConverter.py` (baseline) | gap |
|------|--------|------------------------------|-----|
| 입력 포맷 | `단위:값` | `unit:value` | 일치 |
| 지원 단위 | meter, feet, yard | 동일 | 일치 |
| 변환 비율 | 3.28084 / 1.09361, meter 경유 | 동일 | 일치 |
| 출력 줄 수 | 2줄 (feet, yard) | 3줄 (meter·feet·yard) | **불일치** |
| 출력 반올림 | `8.2`, `2.7` 추정 | raw float | **불일치** |
| 형식 검증 | 거부 | 구현됨 | 일치 |
| 숫자 검증 | (명시 없음) | 구현됤 | 일치 |
| 미지원 단위 | 거부 | 구현됨 | 일치 |
| 음수 검증 | 요구 | 없음 (허용) | **불일치** |
| 테스트 | TC 작성 | 0건 → RED 진행 | gap → **진행 중** |
| OCP/SRP·추가 요구 | 명시 | 미구현 | **범위 외** |

---

## 9. 검증 전략 (TDD)

### SSOT 우선순위

1. PM 미결 확정값
2. **RED 테스트** (미결 항목의 기대값·출력 형태)
3. `report/02_workbook_scope_verification.md`
4. `README.md`
5. `UnitConverter.py` (baseline 참고, 정답 SSOT 아님)

### TDD 사이클

| Phase | 수정 범위 | 완료 조건 |
|-------|----------|----------|
| **RED** | `tests/` only | 추가 테스트 **FAIL** (incomplete는 의도 FAIL + `[미결]` 주석) |
| **GREEN** | `src/` 최소 구현 | 직전 RED 1건 **PASS** |
| **REFACTOR** | `src/` only | 전체 테스트 **PASS** 유지 |

### RED 테스트 목록 (R1 ~ R6)

| ID | 시나리오 | 검증 대상 | 상태 |
|----|----------|----------|------|
| R1 | `meter:2.5` → feet/yard | 변환·반올림 | **작성됨** (`test_convert_all_meter_to_feet_and_yard`) |
| R2 | `feet:3.28084` → meter ≈ 1, 교차 | 역·교차 변환 | 미작성 |
| R3 | `meter:-2.5` | 음수 정책 | 미작성 |
| R4 | `invalid` (콜론 없음) | 형식 오류 | 미작성 |
| R5 | `cubit:1` | 미지원 단위 | 미작성 |
| R6 | `meter:2.5` 출력 줄·포맷 | 출력 형태 | 미작성 |

### R1 테스트 계약 (현재)

```python
# meter:2.5 → feet ≈ 8.2, yard ≈ 2.7 (README 예시 기준)
# [미결: PM] 반올림 규칙 확정 전
assert result["feet"] == pytest.approx(8.2, abs=0.05)
assert result["yard"] == pytest.approx(2.7, abs=0.05)
```

### 금지 사항

- RED 단계에서 `src/`, `UnitConverter.py` 수정
- `pytest.skip`, `pytest.mark.xfail`, assert 완화·삭제
- 수동 5~7회 실행으로 pytest 대체
- PM 미결 항목에 대한 추측 구현

### 실행

```bash
python -m pytest          # 전체 테스트
python -m pytest -v       # 상세 출력
python UnitConverter.py   # CLI (후속 연동)
```

---

## 10. PM 미결 항목 (의사결정 필요)

| # | 항목 | 선택지 | 영향 |
|---|------|--------|------|
| 1 | 마일스톤 in/out | 기본 3단위+TC vs 추가 요구 3개 포함 | M1/M2 경계 |
| 2 | 출력 반올림 | 소수 자릿수·반올림 방식 (README: 1자리 추정) | R1, R6, `format_output` |
| 3 | 출력 형태 | 2줄 vs 3줄, 입력 단위 줄 포함 여부 | R6, CLI 출력 |
| 4 | 음수 정책 | 에러 vs 허용 | R3, `parse_input` |
| 5 | (후속) 동적 등록 UX | 런타임 1회 vs 파일 영구 저장 | M2 |
| 6 | (후속) spec 브랜치 역할 | 설계만 vs 구현 포함 | 브랜치 전략 |

**미결 존재 시 `SCOPE_BEFORE_CODE`**: GREEN·REFACTOR·CLI 연동 금지 (incomplete RED는 허용).

---

## 11. 현재 진행 상태

| 영역 | 상태 | 산출물 |
|------|------|--------|
| Mom Test | ✅ 완료 | 페르소나·증거·진짜 문제 |
| 범위·검증 워크북 | ✅ 완료 | `report/02_workbook_scope_verification.md` |
| Cursor Rules | ✅ 완료 | `.cursorrules` |
| `/export` 명령 | ✅ 완료 | `.cursor/commands/export.md` |
| `/tdd-red` 명령 | ✅ 완료 | `.cursor/commands/tdd-red.md` |
| pytest 환경 | ✅ 완료 | `pyproject.toml` (`pythonpath=["src"]`) |
| 순수 로직 모듈 | 🔶 stub | `src/unit_converter.py` |
| RED 테스트 | 🔶 1/6 | R1만 작성 |
| GREEN 구현 | ⬜ 미착수 | PM 미결 + RED 미완 |
| CLI 연동 | ⬜ 미착수 | `UnitConverter.py` baseline 유지 |
| REFACTOR | ⬜ 미착수 | GREEN 완료 후 |

---

## 12. 마일스톤 로드맵

### M1 — 기본 변환 + TDD (현재)

- 범위·검증 계약 고정 (SC-1~2)
- RED 6건 → GREEN → REFACTOR
- `src/unit_converter.py` 구현 + CLI 연동
- PM 미결 3건(반올림·출력·음수) 확정

### M2 — README 추가 요구 (후속)

- OCP/SRP 설계 리팩토링
- 설정 외부화 (JSON/YAML)
- 동적 단위 등록
- JSON / CSV / 표 출력 포맷

---

## 13. 비기능 요구사항

| 항목 | 요구 |
|------|------|
| 언어 | Python 3.10+ |
| 테스트 프레임워크 | pytest |
| 코드 스타일 | 순수 로직(`src/`)과 CLI(`UnitConverter.py`) 분리 |
| 문서·주석 | 한국어 (코드 식별자·pytest 함수명은 영어) |
| 완료 기준 | `python -m pytest` 전체 PASS (GREEN/REFACTOR 후) |

---

## 14. 참고 문서

| 문서 | 역할 |
|------|------|
| `README.md` | 원본 요구사항·비즈니스 비율·실습 Activities |
| `report/02_workbook_scope_verification.md` | 범위·검증 SSOT, SC-1~3, Test Loop |
| `.cursorrules` | AI·TDD·Phase 규칙, API 계약 |
| `.cursor/commands/tdd-red.md` | RED Phase 실행 가이드 |
| `UnitConverter.py` | CLI baseline (정답 SSOT 아님) |
| `report/0_export_report_*.md`, `report/1_export_report_*.md` | 세션 이력 |

---

## 15. 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| 1.0 | 2026-06-11 | Mom Test·워크북·TDD 진행 상태 기반 초안 작성 |
