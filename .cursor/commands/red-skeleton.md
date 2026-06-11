# /red-skeleton — ARRR A단계 (RED ④) pytest.fail 스켈레톤

`/red-test-plan` 블록 1~3 설계표를 **`pytest.fail` 스켈레톤**으로 `tests/`에만 반영한다.  
도메인 호출·assert 본문·GREEN 구현은 **`/tdd-red`** (RED ⑤)에서 교체.

**프로젝트:** UnitConverter_08 — `src/unit_converter.py` (Logic) · `UnitConverter.py` (boundary UI)

## 1. 역할·범위

| 항목 | 내용 |
|------|------|
| ARRR | **A**sk — RED 사이클 **④** (스켈레톤 작성) |
| 선행 | `/red-test-plan` — C2C·Track B·블록 3 테스트 플랜 |
| 후속 | `/tdd-red` — `pytest.fail` → `assert` / `pytest.raises` |
| 수정 허용 | **`tests/`만** (`test_*.py`, `tests/conftest.py`) |
| 수정 금지 | `src/` · `UnitConverter.py` · GREEN/REFACTOR |

| Track | Layer | 대상 |
|-------|-------|------|
| Logic (기본) | `entity` | `tests/test_unit_converter.py` — `parse_input` / `to_meters` / `convert_all` / `format_output` |
| UI | `boundary` | `tests/test_unit_converter_cli.py` (플랜 시) — `UnitConverter.main` · stdout |

## 2. SSOT (읽기)

1. **직전 `/red-test-plan` 응답** — Test ID · 함수명 · G/W/T · 파일 경로
2. 채팅에 플랜 없으면 → `/red-test-plan` 규칙으로 **자동 추출** (R1~R6 다음 1건)
3. `doc/PRD.md` · `.cursorrules` · `report/02_workbook_scope_verification.md`

추가 입력 없이 `/red-skeleton` 만으로 동작. Test ID·함수명을 사용자에게 묻지 않는다.

### Test ID — 다음 스켈레톤 대상

| Test ID | 대상 함수 | 시나리오 | `tests/` 상태 |
|---------|----------|----------|---------------|
| R1 | `convert_all` | `meter:2.5` → feet/yard | assert RED **이미 있음** — 스켈레톤 대상 아님 |
| R2 | `to_meters` | `feet:3.28084` → meter ≈ 1 | **다음 후보** |
| R3 | `parse_input` | `meter:-2.5` 음수 | 미작성 |
| R4 | `parse_input` | `invalid` 형식 | 미작성 |
| R5 | `parse_input` | `cubit:1` 미지원 단위 | 미작성 |
| R6 | `format_output` | `meter:2.5` 출력 형태 | 미작성 |

## 3. Phase 선언 (필수)

응답 **첫 줄**:

```text
Phase: red | Layer: entity | Track: Logic
```

- `Phase: red` 소문자 — GREEN/REFACTOR 혼용 금지.
- CLI Track: `Phase: red | Layer: boundary | Track: UI`

## 4. 스켈레톤 규칙

### 4.1 AAA 주석

| 블록 | 주석 | 내용 |
|------|------|------|
| **Given** | `# Given — …` | Arrange — 입력 문자열·단위·값 **리터럴** 또는 conftest 픽스처 |
| **When** | `# When — …` | 호출 예정 API 1개 (실제 호출 **금지**) |
| **Then** | `# Then — …` + **한 줄** | `pytest.fail("RED: {Test ID} — …")` **만** |

기존 `/tdd-red`·R1의 `# Arrange` / `# Act` / `# Assert` 주석은 **스켈레톤 신규 작성 시** `# Given` / `# When` / `# Then` 으로 통일.

### 4.2 Then — 유일한 실행 assert

```python
pytest.fail("RED: R2 — to_meters(feet, 3.28084) ≈ 1.0 meter")
```

| 허용 | 금지 |
|------|------|
| `pytest.fail("RED: {Test ID} — …")` **1줄** | `assert` · `pytest.raises` · `pytest.approx` |
| Given/When에 `# [미결: PM]` | `pytest.skip` · `pytest.mark.xfail` |
| Arrange 지역 변수·픽스처 | `pass` · 통과 더미 · `return` 우회 |
| `import pytest` | `from unit_converter import …` 후 **실제 호출** |
| | Domain Mock · E001~E005 emit |

스켈레톤 RED 완료 = 해당 test **FAILED** (`pytest.fail` 메시지).

### 4.3 RED 1회

- **test 함수 1개 · Test ID 1개** — 플랜·`/tdd-red`와 동일.
- R1(`test_convert_all_meter_to_feet_and_yard`)처럼 assert RED가 이미 있으면 **스킵** → R2~R6 순차.

## 5. Arrange 데이터 · conftest (UnitConverter)

프로덕션 `src/`·`unit_converter` **import·호출 금지**. Arrange는 **테스트 측 데이터만**.

### 5.1 확정 상수 (PRD · `.cursorrules`)

| 이름 | 값 | 용도 |
|------|-----|------|
| `METER_TO_FEET` | `3.28084` | Given 리터럴 · conftest |
| `METER_TO_YARD` | `1.09361` | Given 리터럴 · conftest |
| 지원 단위 | `meter`, `feet`, `yard` | Given |
| 입력 포맷 | `unit:value` | R3~R5 Given 문자열 |

- **`src/unit_converter.py`에서 상수 import 금지** — GREEN 전 stub 호출·우발 의존 방지.
- 필요 시 `tests/conftest.py`에 **픽스처 데이터만** 중복 정의 (프로덕션과 동일 숫자, 테스트 전용).

### 5.2 conftest (`tests/conftest.py`)

| 규칙 | 내용 |
|------|------|
| 생성 | 플랜·Given 재사용 필요 시만. **없어도 됨** — Arrange 리터럴로 충분하면 생략 |
| 내용 | `@pytest.fixture` — 튜플·문자열 등 **순수 데이터**만 |
| 금지 | `unit_converter` import · 도메인 함수 호출 · Mock |

```python
# tests/conftest.py — 예: R2 Given 재사용 (선택)
import pytest

METER_TO_FEET = 3.28084
METER_TO_YARD = 1.09361


@pytest.fixture
def feet_one_meter_pair():
    """feet 3.28084 ≈ 1 meter — R2 Arrange."""
    return "feet", 3.28084
```

### 5.3 스켈레톤 템플릿 — Logic Track

**파일:** `tests/test_unit_converter.py`

```python
import pytest


def test_to_meters_feet_to_meter():
    # Given — unit=feet, value=3.28084 (1 meter = 3.28084 feet)
    unit, value = "feet", 3.28084
    # When — to_meters(unit, value) → meter ≈ 1.0
    # Then — 스켈레톤 RED (/tdd-red에서 assert·import 교체)
    pytest.fail("RED: R2 — to_meters(feet, 3.28084) ≈ 1.0 meter")
```

**R3 (incomplete) 예:**

```python
def test_parse_input_negative_meter_policy():
    # Given — raw="meter:-2.5"
    # [미결: PM] 음수 = 에러 vs 허용
    raw = "meter:-2.5"
    # When — parse_input(raw)
    # Then
    pytest.fail("RED: R3 — parse_input negative meter policy [미결: PM]")
```

**R4 예:**

```python
def test_parse_input_rejects_missing_colon():
    # Given — raw="invalid" (콜론 없음)
    raw = "invalid"
    # When — parse_input(raw) → ValueError
    # Then
    pytest.fail("RED: R4 — parse_input rejects missing colon")
```

### 5.4 boundary Track (선택)

Layer·Track만 `boundary` / `UI`로 바꾸고 동일 스켈레톤 규칙 적용.

```python
# tests/test_unit_converter_cli.py — 예 (파일·함수명은 플랜 따름)
import pytest


def test_cli_meter_input_prints_conversions(capsys):
    # Given — stdin "meter:2.5"
    # When — main() (구현 전)
    # Then
    pytest.fail("RED: U1 — CLI meter:2.5 output lines [미결: PM]")
```

## 6. 작업 절차

1. `/red-test-plan` 또는 PRD에서 **Test ID 1건** · 함수명 · 파일 경로 확인.
2. `tests/conftest.py` — 픽스처 필요 시만 추가 (§5.2).
3. `tests/test_unit_converter.py` — AAA + `pytest.fail` **1줄** 추가.
4. pytest 실행 · 스켈레톤 보고.

```bash
python -m pytest tests/test_unit_converter.py::<함수명> -v
```

**기대:** `FAILED` — `pytest.fail: RED: …`  
**PASSED면 실패** — `pytest.fail` 누락·skip·더미 확인.

## 7. 완료 보고

```markdown
Phase: red | Layer: entity | Track: Logic

## 스켈레톤 보고
| 항목 | 내용 |
|------|------|
| Test ID | R? |
| 테스트 | `test_...` |
| pytest 결과 | FAILED — RED: … (한 줄) |
| 변경 파일 | `tests/...` only |
```

**완료 한 줄 (응답 마지막):**

```text
/tdd-red 로 assert 교체 준비됐다
```

## 8. 금지

| 금지 | 이유 |
|------|------|
| `src/` · `UnitConverter.py` 수정 | GREEN Phase |
| `from unit_converter import …` + **호출** | `/tdd-red`까지 보류 |
| Then에 `assert` / `pytest.raises` | `/tdd-red` |
| `pytest.skip` · `xfail` · 통과 더미 | RED 우회 |
| Domain Mock · E001~E005 | `/red-test-plan` 블록 4 |
| GREEN / REFACTOR | Phase: red 만 |
| R1 재스켈레톤 (assert RED 존재) | 이미 `/tdd-red` 수준 |

## 9. `/tdd-red` 와 차이

| | `/red-skeleton` (④) | `/tdd-red` (⑤) |
|---|---------------------|----------------|
| Then | `pytest.fail("RED: …")` only | `assert` / `pytest.raises` |
| import | `pytest` only | `from unit_converter import …` |
| When | 주석만 | 함수 1회 **실제 호출** |
| Arrange 상수 | tests 리터럴·conftest | 동일 + 도메인 호출 |
| 실패 원인 | 의도적 fail 메시지 | stub·assert FAIL |

## 10. 완료 체크

- [ ] 첫 줄 `Phase: red | Layer: … | Track: …`
- [ ] AAA `# Given` / `# When` / `# Then`
- [ ] Then = `pytest.fail("RED: {Test ID} — …")` **1줄만**
- [ ] assert · skip · xfail · `unit_converter` 호출 없음
- [ ] `src/` · `UnitConverter.py` 수정 0건
- [ ] `python -m pytest` **FAILED** 확인
- [ ] 스켈레톤 보고 (Test ID · FAIL 한 줄 · `tests/`만)

## 11. 관련 Command

| Command | Phase | 산출 |
|---------|-------|------|
| `/red-test-plan` | RED ③ | C2C·플랜 (파일 없음) |
| `/red-skeleton` | RED ④ | `pytest.fail` 스켈레톤 |
| `/tdd-red` | RED ⑤ | assert·도메인 호출 RED |
