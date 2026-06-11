# /tdd-red — UnitConverter RED 단계 (tests/ 전용)

`src/unit_converter.py` TDD **RED** Phase 전용. 실패하는 pytest 1건을 추가한다.

## 1. Phase 선언

응답 **첫 줄**에 반드시 선언:

```text
[Phase: RED]
```

- `GREEN` / `REFACTOR` 혼용 금지.
- RED 완료 = 추가한 테스트가 `pytest`에서 **FAIL** (incomplete는 의도 FAIL + `[미결]`).

## 2. RED 1회 규칙

| 항목 | 규칙 |
|------|------|
| 범위 | **test 함수 1개 · 시나리오 1개 · assert ≥1** |
| 수정 허용 | `tests/` (`test_*.py`, `conftest.py`, 헬퍼) |
| SC-3 매핑 | R1~R6 중 **1개**만 이번 RED 대상 (중복·뭉침 금지) |

### SC-3 — R1~R6 후보

| ID | 시나리오 | 검증 대상 |
|----|----------|----------|
| R1 | `meter:2.5` → feet/yard | 변환·반올림 |
| R2 | `feet:3.28084` → meter ≈ 1, 교차 | 역·교차 변환 |
| R3 | `meter:-2.5` | 음수 정책 |
| R4 | `invalid` (콜론 없음) | 형식 오류 |
| R5 | `cubit:1` | 미지원 단위 |
| R6 | `meter:2.5` 출력 줄·포맷 | 출력 형태 |

PM 미결(R1·R3·R6 등)은 `# [미결: PM]` 주석 + 명시적 기대값. skip·xfail 금지.

## 3. AAA 절차

각 RED 테스트는 **Arrange → Act → Assert** 순서로 작성.

```python
def test_<대상>_<시나리오>():
    # Arrange — 입력·상수·기대값 준비
    ...

    # Act — 테스트 대상 함수 1회 호출
    ...

    # Assert — 기대와 실제 비교 (완화·삭제 금지)
    ...
```

- **Arrange**: SSOT(RED 테스트 > report/02 > README) 기준 기대값.
- **Act**: `parse_input` / `to_meters` / `convert_all` / `format_output` 중 **1개**만.
- **Assert**: `pytest.raises(ValueError)` 또는 `==` / `approx`. `pass`·빈 assert 금지.

## 4. pytest 예시

### R1 — 변환 (확정 비율)

```python
import pytest
from unit_converter import convert_all


def test_convert_all_meter_to_feet_and_yard():
    # Arrange
    unit, value = "meter", 2.5
    # [미결: PM] 반올림 규칙 확정 전 — README 예시 8.2 / 2.7 기준

    # Act
    result = convert_all(unit, value)

    # Assert
    assert result["feet"] == pytest.approx(8.2, abs=0.05)
    assert result["yard"] == pytest.approx(2.7, abs=0.05)
```

### R4 — 형식 오류 (확정: ValueError)

```python
import pytest
from unit_converter import parse_input


def test_parse_input_rejects_missing_colon():
    # Arrange
    raw = "invalid"

    # Act & Assert
    with pytest.raises(ValueError, match="format|Invalid"):
        parse_input(raw)
```

### R3 — incomplete (음수, PM 미결)

```python
import pytest
from unit_converter import parse_input


def test_parse_input_negative_meter_policy():
    # Arrange
    raw = "meter:-2.5"
    # [미결: PM] 음수 = 에러 vs 허용 — PM 확정 시 기대값 갱신

    # Act & Assert — placeholder: 에러 기대 (PM 확정 전 의도 FAIL 가능)
    with pytest.raises(ValueError):
        parse_input(raw)
```

## 5. 실행·검증

```bash
python -m pytest tests/test_unit_converter.py::<함수명> -v
```

- **기대 결과**: `FAILED` (또는 incomplete — 의도 FAIL + `[미결]` 주석).
- `PASSED`면 RED 아님 — assert·기대값 재검토 (구현 수정 금지).

## 6. 보고 형식

RED 작업 후 응답에 아래 포함:

```markdown
[Phase: RED]

## RED 보고
| 항목 | 내용 |
|------|------|
| SC-3 ID | R? |
| 테스트 | `test_...` |
| 대상 API | `parse_input` / `to_meters` / `convert_all` / `format_output` |
| 시나리오 | (한 줄) |
| [미결] | 있음 / 없음 |
| pytest 결과 | FAILED — (한 줄 이유) |
| 수정 파일 | `tests/...` only |
```

## 7. 금지

| 금지 | 이유 |
|------|------|
| `src/`, `UnitConverter.py` 수정 | GREEN Phase |
| assert 완화·삭제·`approx` 범위 임의 확대 | RED 우회 |
| `pytest.skip`, `pytest.mark.xfail` | incomplete는 주석으로 |
| 한 test에 R1+R2 등 **다중 시나리오** | 1 RED = 1 시나리오 |
| 수동 실행으로 RED 대체 | SC-3 pytest 선행 |
| `pyproject.toml`, `.cursorrules`, `README.md`, `report/` 수정 | RED 범위 밖 |

## 8. 완료 체크

- [ ] 응답 첫 줄 `[Phase: RED]`
- [ ] `tests/`만 수정
- [ ] AAA + assert ≥1
- [ ] SC-3 R? 1건 매핑
- [ ] `pytest` **FAILED** 확인
- [ ] RED 보고 표 작성
