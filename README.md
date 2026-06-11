# Unit Converter (Python)

![unit-converter](./unit-converter.jpg)

길이 단위(`meter` / `feet` / `yard`)를 `단위:값` 형식으로 입력받아 변환 결과를 출력하는 CLI 프로젝트입니다.

> **상세 요구사항·범위·검증 계약** → [`doc/PRD.md`](doc/PRD.md)  
> **범위·성공 기준 SSOT** → [`report/02_workbook_scope_verification.md`](report/02_workbook_scope_verification.md)

---

## 현재 상태 (2026-06-11)

| 항목 | 상태 |
|------|------|
| 프로젝트 | **UnitConverter_08** (GitHub·문서 공식명) |
| 마일스톤 | **M1** — 기본 변환 + TDD |
| 순수 로직 (`src/unit_converter.py`) | stub (미구현) |
| CLI (`UnitConverter.py`) | 36줄 프로토타입 baseline |
| pytest | RED R1 1건 작성 (R2~R6 미작성) |
| ARRR Cursor Commands | `red-test-plan` · `red-skeleton` · `tdd-red` · `green-minimal` · `golden-master` · `refactor-smell` |
| PM 미결 | 출력 반올림·줄 수, 음수 정책 |

완료 기준: `python -m pytest` 전체 PASS (GREEN/REFACTOR 후)

---

## Overview

- 사용자가 입력한 길이(`단위:값`)를 기반으로 meter / feet / yard로 변환해 출력합니다.
- 변환 로직은 `src/unit_converter.py`에, CLI 진입점은 `UnitConverter.py`에 분리합니다.
- **pytest RED → GREEN → REFACTOR** 순서로 구현·검증합니다.
- 생성형 AI·Cursor 슬래시 명령어로 ARRR 단계(설계 → RED → GREEN → Refine)를 지원합니다.

---

## 빠른 시작

### 가상환경

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# pytest 설치 (미설치 시)
pip install pytest

# 가상환경 비활성화
deactivate
```

### 실행

```bash
# 테스트 (완료 기준)
python -m pytest
python -m pytest -v

# 단일 RED 테스트
python -m pytest tests/test_unit_converter.py::test_convert_all_meter_to_feet_and_yard -v

# CLI (프로토타입 baseline)
python UnitConverter.py
```

---

## 프로젝트 구조

```
UnitConverter_08/          # GitHub 저장소명; 로컬 clone 폴더는 UnitConverter_09 등 가능
├── src/
│   ├── unit_converter.py   # 순수 변환 로직 (구현 대상)
│   └── constants.py          # 비즈니스 상수 SSOT (GREEN 시 생성)
├── tests/
│   └── test_unit_converter.py
├── UnitConverter.py            # CLI 진입점 (baseline, 후속 연동)
├── doc/PRD.md                  # 제품 요구사항 문서
├── report/02_workbook_scope_verification.md
├── .cursor/
│   └── commands/               # ARRR·TDD 슬래시 명령어
├── .cursorrules                # TDD·API 규칙
└── pyproject.toml              # pythonpath=["src"]
```

---

## 마일스톤 M1 — 기본 요구사항 (현재)

### 입력·출력

입력 예시:

```
meter:2.5
```

목표 출력 (README 예시 — **반올림·줄 수 PM 미결**):

```
2.5 meter = 8.2 feet
2.5 meter = 2.7 yard
```

> 현재 `UnitConverter.py` baseline은 **3줄**(meter·feet·yard) 출력, **raw float**입니다.  
> 최종 형태는 PM 확정 후 RED 테스트(R6)가 SSOT입니다.

### 지원 단위

- `meter`
- `feet`
- `yard`

### 입력 검증

| 조건 | 동작 | 상태 |
|------|------|------|
| 잘못된 형식 (콜론 없음) | `ValueError` | 확정 |
| 숫자 파싱 실패 | `ValueError` | 확정 |
| 미지원 단위 (예: `cubit`) | `ValueError` | 확정 |
| 음수 | 에러 vs 허용 | **[미결] PM** |

### 비즈니스 로직 (확정)

| 상수 | 값 |
|------|-----|
| `METER_TO_FEET` | `3.28084` |
| `METER_TO_YARD` | `1.09361` |

- **모든 변환은 meter 중간값을 경유**합니다.
- feet ↔ yard 비율도 meter 기준으로 계산합니다.
- GREEN 단계에서 상수는 `src/constants.py`에만 둡니다 (함수 내부 매직넘버 금지).

### API (`src/unit_converter.py`)

```
parse_input(input_str) -> tuple[str, float]
to_meters(unit, value) -> float
convert_all(unit, value) -> dict[str, float]   # keys: meter, feet, yard
format_output(unit, value, converted) -> list[str]
```

형식·숫자·미지원 단위 오류 시 `ValueError`(메시지 포함). E001~E005 에러코드는 사용하지 않습니다.

---

## 검증 (TDD)

### SSOT 우선순위

1. PM 미결 확정값
2. RED 테스트 (`tests/`)
3. `report/02_workbook_scope_verification.md`
4. [`doc/PRD.md`](doc/PRD.md)
5. 본 README (비즈니스 비율·기본 요구)
6. `UnitConverter.py` (baseline 참고, 정답 SSOT 아님)

### TDD 사이클

| Phase | 수정 범위 | 완료 조건 |
|-------|----------|----------|
| **RED** | `tests/` only | 추가 테스트 **FAIL** |
| **GREEN** | `src/` 최소 구현 | 직전 RED 1건 **PASS** |
| **REFACTOR** | `src/` only | 전체 테스트 **PASS** 유지 |

### ARRR Cursor Commands (M1 파이프라인)

| Command | ARRR 단계 | 역할 |
|---------|-----------|------|
| [`red-test-plan`](.cursor/commands/red-test-plan.md) | Ask RED ③ | C2C·테스트 플랜 (파일 생성 없음) |
| [`red-skeleton`](.cursor/commands/red-skeleton.md) | Ask RED ④ | `pytest.fail` 스켈레톤 (`tests/` only) |
| [`tdd-red`](.cursor/commands/tdd-red.md) | RED ⑤ | assert·도메인 호출 RED |
| [`green-minimal`](.cursor/commands/green-minimal.md) | Respond GREEN | RED 1묶음당 `src/` 최소 구현 |
| [`golden-master`](.cursor/commands/golden-master.md) | GREEN+ | Approval Test · golden 스냅샷 |
| [`refactor-smell`](.cursor/commands/refactor-smell.md) | Refine ⑦ | 코드 스멜 탐지 (수정 없음) |

권장 순서: `red-test-plan` → `red-skeleton` → `tdd-red` → `green-minimal` → (선택) `golden-master` → `refactor-smell`

### RED 테스트 (R1 ~ R6)

| ID | 시나리오 | 대상 API | 상태 |
|----|----------|----------|------|
| R1 | `meter:2.5` → feet/yard 변환·반올림 | `convert_all` | **작성됨** |
| R2 | `feet:3.28084` → meter ≈ 1, 교차 변환 | `to_meters` | 미작성 |
| R3 | `meter:-2.5` → 음수 정책 | `parse_input` | 미작성 `[미결: PM]` |
| R4 | `invalid` → 형식 오류 | `parse_input` | 미작성 |
| R5 | `cubit:1` → 미지원 단위 | `parse_input` | 미작성 |
| R6 | `meter:2.5` → 출력 줄·포맷 | `format_output` | 미작성 `[미결: PM]` |

SC-3 목표: R1~R6 각 1 test (≥6건) 선행 후 GREEN.

---

## 마일스톤 M2 — 추가 요구사항 (후속)

아래는 **M1 범위 외**입니다. M1 완료 후 진행합니다.

### 품질·설계

- OCP를 만족하는 설계
- SRP를 만족하는 클래스 구성

### 기능

- **설정 외부화** — 변환 비율을 JSON/YAML에서 로드
- **동적 단위 등록** — 예: `1 cubit = 0.4572 meter` 런타임 등록
- **출력 포맷 선택** — JSON / CSV / 표 형태

새 단위 추가 시 기존 코드 변경을 최소화하는 구조를 목표로 합니다.

---

## PM 미결 항목

| # | 항목 | 영향 |
|---|------|------|
| 1 | 출력 반올림 (소수 자릿수·방식) | R1, R6, `format_output` |
| 2 | 출력 형태 (2줄 vs 3줄, 입력 단위 포함) | R6, CLI |
| 3 | 음수 입력 (에러 vs 허용) | R3, `parse_input` |

확정 전 `src/` 구현 추측 금지. incomplete RED는 `# [미결: PM]` 주석으로 기록합니다.

---

## 참고 문서

| 문서 | 설명 |
|------|------|
| [`doc/PRD.md`](doc/PRD.md) | 제품 요구사항·범위·로드맵 |
| [`report/02_workbook_scope_verification.md`](report/02_workbook_scope_verification.md) | SC-1~3, Test Loop |
| [`.cursorrules`](.cursorrules) | TDD Phase·API 계약 |
| [`.cursor/commands/`](.cursor/commands/) | ARRR·TDD 슬래시 명령어 모음 |

---

## 생성형 AI를 활용한 Activities (6시간)

실습 흐름을 M1/M2 마일스톤과 TDD에 맞게 정리했습니다.

1. **문제 코드 및 요구사항 분석** (0.5시간)
   - README vs `UnitConverter.py` gap 파악
   - Mom Test — 범위·검증 기준 미정 pain point 도출
2. **범위·검증 계약 고정** (0.5시간)
   - in/out 확정, PM 미결 항목 정리 (`doc/PRD.md`, `report/02`)
3. **TDD — RED → GREEN → REFACTOR** (2.5시간)
   - `/red-test-plan`으로 C2C 설계 → `/red-skeleton`·`/tdd-red`로 RED 6건
   - `/green-minimal`로 `src/unit_converter.py` 최소 구현 → CLI 연동
4. **추가 요구사항 (M2)** (2시간)
   - OCP/SRP, 설정 외부화, 동적 등록, 출력 포맷 + TC
5. **회고 및 발표** (0.5시간)
   - 실습 목표와 달성도
   - AI 활용 — 도움이 된 순간과 한계
   - TC 추가가 개선에 미친 영향, TC 작성 팁
   - 클린코드·리팩토링에서 느낀 장점과 어려운 점
