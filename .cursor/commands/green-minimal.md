# /green-minimal — ARRR R단계 (Respond = GREEN) 최소 구현

**RED 1묶음**(Test ID 1개)당 `src/` **최소 구현**만 추가한다.  
**1 커밋 = 1 RED 묶음** — `git commit`은 **사용자 명시 요청 시만**.

**프로젝트:** UnitConverter_09 — `src/` (Logic) · `UnitConverter.py` (boundary, GREEN 후속)

## 1. 역할·범위

| 항목 | 내용 |
|------|------|
| ARRR | **R**espond — GREEN (TDD Respond) |
| 선행 | `/tdd-red` 또는 `/red-skeleton` + `/tdd-red` — **FAILED** RED 1건 |
| 후속 | 다음 RED 묶음 · 또는 `/refactor-*` (별도 Command) |
| 수정 허용 | **`src/`** (+ 해당 RED의 `tests/` — `pytest.fail` → assert 교체) |
| 수정 금지 | 이번 Test ID **외** RED 동시 해결 · REFACTOR · assert 완화 |

| Track | Layer | 구현 위치 |
|-------|-------|----------|
| Logic (기본) | `entity` | `src/constants.py` · `src/unit_converter.py` |
| UI | `boundary` | `UnitConverter.py` — Layer·Track만 변경 |

## 2. SSOT (읽기)

1. **대상 test 함수** — Test ID · Given/When/Then · assert 계약
2. `doc/PRD.md` · `.cursorrules` · `report/02_workbook_scope_verification.md`
3. PM 미결: `[미결: PM]` — **추측 구현 금지**. RED가 incomplete면 GREEN **보류**·PM 확인

## 3. Phase 선언 (필수)

응답 **첫 줄**:

```text
Phase: green | Layer: entity | Track: Logic
```

- `Phase: green` 소문자 — RED/REFACTOR 혼용 금지.
- CLI: `Phase: green | Layer: boundary | Track: UI`

## 4. 절차 (RED 1묶음)

| Step | 작업 | 완료 조건 |
|------|------|----------|
| **① RED 재확인** | 대상 test 1개만 실행 | **FAILED** (assert FAIL 또는 `pytest.fail`) |
| **② 최소 구현** | `src/` — 이번 Test ID 통과에 **필요한 코드만** | 매직넘버·하드코딩 없음 → `constants.py` |
| **③ 테스트 정리** | `pytest.fail` 제거 → `/tdd-red` assert·Act·import 반영 | test 본문이 RED 계약과 일치 |
| **④ PASS 확인** | 단일 test → 파일 전체 pytest | 대상 **PASS** · **회귀 0** |

### ④ 회귀 규칙

- 파일 전체 pytest에서 **기존 PASS test가 FAIL** → 즉시 원인 수정 (assert 완화 **금지**).
- 다른 Test ID를 “겸사겸사” 해결하지 않음 — **이번 RED 묶음만**.

## 5. `src/constants.py` SSOT

변환 비율·지원 단위 등 **비즈니스 상수**는 `src/constants.py`에만 둔다.

```python
# src/constants.py — SSOT (PRD · .cursorrules 확정값)
METER_TO_FEET = 3.28084
METER_TO_YARD = 1.09361

SUPPORTED_UNITS = frozenset({"meter", "feet", "yard"})
```

| 허용 | 금지 |
|------|------|
| `unit_converter.py`에서 `from constants import …` | 함수·모듈 내부 `3.28084` 리터럴 |
| GREEN에 **필요한 상수만** 추가 | README/PRD에 없는 임의 비율 |
| tests Arrange 리터럴 (RED 계약) | tests에서 `src` 상수 import로 assert 대체 |

`constants.py`가 없으면 **이번 GREEN에서 생성** — 최소 diff.

## 6. ECB · E001~E005

### 6.1 entity Layer (Logic)

| 규칙 | 내용 |
|------|------|
| **ECB** | **E**rror — `ValueError` (형식·숫자·미지원 단위). **C**ontract — PRD API·dict 키. **B**oundary — `unit:value` 문자열 파싱 |
| **import 금지** | `UnitConverter.py` · CLI · stdout/stdin · **control** 계층 |
| **의존 방향** | `constants` ← `unit_converter` — entity만 |

### 6.2 E001~E005

| 금지 | 대신 |
|------|------|
| `raise E001` … `E005` | `ValueError("…")` — 메시지 포함 |
| `return {"code": "E00x"}` | 예외 또는 정상 반환 (PRD 계약) |
| 테스트·구현에 E001~E005 문자열 **emit** | 도메인 의미 있는 메시지 |

## 7. 최소 구현 가이드 (Logic · Test ID별)

**원칙:** 이번 test가 호출하는 **함수·분기만** 구현. 나머지 API는 stub 유지.

| Test ID | 최소 구현 범위 |
|---------|---------------|
| R1 | `convert_all` + meter 경유 · `constants` |
| R2 | `to_meters` (feet 분기) + `constants` |
| R3 | `parse_input` — 음수 분기 (**PM 확정 후만**) |
| R4 | `parse_input` — 콜론·형식 `ValueError` |
| R5 | `parse_input` — 미지원 단위 `ValueError` |
| R6 | `format_output` (**PM 확정 후만**) |

### R2 GREEN 예 (요지)

```python
# src/unit_converter.py
from constants import METER_TO_FEET, METER_TO_YARD, SUPPORTED_UNITS


def to_meters(unit: str, value: float) -> float:
    if unit == "meter":
        return value
    if unit == "feet":
        return value / METER_TO_FEET
    if unit == "yard":
        return value / METER_TO_YARD
    raise ValueError(f"Unknown unit: {unit}")
```

```python
# tests — pytest.fail 제거 후 (/tdd-red 계약)
def test_to_meters_feet_to_meter():
    # Given
    unit, value = "feet", 3.28084
    # Act
    result = to_meters(unit, value)
    # Assert
    assert result == pytest.approx(1.0)
```

## 8. pytest 명령

```bash
# ① 단일 테스트 (대상 RED 1묶음)
python -m pytest tests/test_unit_converter.py::test_to_meters_feet_to_meter -v

# ② 파일 전체 (회귀 확인)
python -m pytest tests/test_unit_converter.py -v
```

- **① PASS** 후 **② 전체 PASS** — GREEN 완료.
- ②에서 다른 test FAIL → §4 회귀 규칙.

## 9. git commit

| 규칙 | 내용 |
|------|------|
| 시점 | 사용자가 **명시적으로** commit 요청할 때만 |
| 범위 | **1 커밋 = 1 RED 묶음** (해당 test + 최소 `src/` + `constants` diff) |
| 금지 | hook 우회 (`--no-verify`) · 사용자 미요청 commit |

커밋 메시지 예: `green: R2 — to_meters feet to meter`

## 10. 금지

| 금지 | 이유 |
|------|------|
| 이번 Test ID **외** RED 동시 PASS 목적 구현 | 1묶음 원칙 |
| REFACTOR (구조 개선·OCP 전면) | 별도 Phase |
| assert 완화·삭제 · `approx` 범위 확대 | RED 우회 |
| `pytest.skip` · `xfail` | incomplete는 PM 대기 |
| `[미결: PM]` 항목 추측 GREEN | SCOPE_BEFORE_CODE |
| entity → boundary/control import | ECB |
| E001~E005 raise/return/emit | 프로젝트 계약 |
| 매직넘버 (constants 우회) | SSOT |
| `UnitConverter.py` 연동 (Logic Track) | boundary GREEN 별도 |

## 11. 완료 보고

```markdown
Phase: green | Layer: entity | Track: Logic

## GREEN 보고
| 항목 | 내용 |
|------|------|
| Test ID | R? |
| pytest (단일) | PASS — `test_...` |
| pytest (파일) | PASS — N passed / 회귀 없음 |
| 변경 파일 | `src/constants.py`, `src/unit_converter.py`, `tests/...` |
| [미결] | 없음 / (있으면 GREEN 보류 사유) |
| 회귀 | 없음 / (있었으면 수정 내역 한 줄) |
```

- **회귀 실패** 발생 시: 보고 전 **반드시 수정** 후 재실행 결과 기록.
- 커밋은 수행했을 때만 보고에 `commit: (hash 또는 메시지)` 추가.

**완료 한 줄 (응답 마지막):**

```text
다음 RED 묶음 또는 REFACTOR Command로 진행 가능
```

## 12. 완료 체크

- [ ] 첫 줄 `Phase: green | Layer: … | Track: …`
- [ ] ① RED 재확인 (대상 test FAILED였음)
- [ ] ② `src/` 최소 구현 · `constants.py` SSOT
- [ ] ③ `pytest.fail` 제거 · assert·Act 일치
- [ ] ④ 단일 + 파일 pytest **PASS**
- [ ] ECB · E001~E005 · 이번 ID 외 구현 없음
- [ ] git commit — 사용자 요청 시만

## 13. 관련 Command

| Command | Phase | 산출 |
|---------|-------|------|
| `/red-test-plan` | Ask ③ | 플랜 |
| `/red-skeleton` | Ask ④ | `pytest.fail` |
| `/tdd-red` | RED ⑤ | assert RED |
| `/green-minimal` | **Respond (GREEN)** | `src/` 최소 구현 + PASS |
