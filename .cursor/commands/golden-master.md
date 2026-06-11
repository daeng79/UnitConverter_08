# /golden-master — GREEN PASS 후 Golden Master (Approval Test)

대상 **Test ID**가 `/green-minimal` **pytest PASS**된 뒤, **승인 스냅샷**(golden)을 생성·검증한다.  
구현 변경은 golden **재생성** (`UPDATE_GOLDEN=1`) 으로만 반영 — **golden 수동 편집으로 통과 우회 금지**.

**프로젝트:** UnitConverter_08 — Logic Track 기본 · boundary는 Layer만 변경

## 1. 역할·범위

| 항목 | 내용 |
|------|------|
| ARRR | **R**espond — GREEN 직후 **Approval Test** 구축 |
| 선행 | `/green-minimal` — 대상 Test ID **PASS** |
| 수정 허용 | `tests/_approval.py` · `tests/golden/` · 대상 test에 golden hook **1묶음** |
| 수정 금지 | `src/` (golden만으로 구현 우회) · golden **수동** 수정 · assert 완화 |

| Track | Layer | golden 용도 |
|-------|-------|-------------|
| Logic | `entity` | `convert_all` / `format_output` / `ValueError` 메시지 스냅샷 |
| UI | `boundary` | CLI stdout 스냅샷 (별도 `{id}.approved.txt`) |

## 2. 전제

- 대상 Test ID의 pytest가 **이미 PASS** (`/green-minimal` 완료).
- `[미결: PM]` RED는 GREEN·golden **보류**.
- **1 golden = 1 Test ID** — 이번 ID 외 golden 일괄 갱신 금지.

## 3. Phase 선언 (필수)

응답 **첫 줄**:

```text
Phase: green | Layer: entity | Track: Logic
```

## 4. 절차

| Step | 작업 | 완료 조건 |
|------|------|----------|
| **0** | 대상 test PASS 재확인 | `pytest …::test_…` **PASSED** |
| **1** | `tests/_approval.py` — `assert_matches_golden` (없으면 **생성**) | import 가능 |
| **2** | `tests/golden/{id}.approved.txt` 연결 | test에서 `golden_id` 지정 |
| **3** | `UPDATE_GOLDEN=1 pytest …` | golden **기준 파일 생성** |
| **4** | `UPDATE_GOLDEN` **없이** 동일 pytest | **matched** (PASS) |

### Step 1 — `tests/_approval.py`

없으면 생성. **헬퍼만** — 도메인 로직 없음.

```python
# tests/_approval.py
import os
from pathlib import Path

GOLDEN_DIR = Path(__file__).resolve().parent / "golden"


def assert_matches_golden(actual: str, golden_id: str) -> None:
    """Approval Test — actual vs tests/golden/{golden_id}.approved.txt"""
    path = GOLDEN_DIR / f"{golden_id}.approved.txt"
    if os.environ.get("UPDATE_GOLDEN") == "1":
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(actual, encoding="utf-8", newline="\n")
        return
    if not path.is_file():
        raise AssertionError(f"golden missing: {path}")
    expected = path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(
            f"golden mismatch: {golden_id}\n"
            f"--- expected ({path}) ---\n{expected}"
            f"--- actual ---\n{actual}"
        )


def format_int_array_1_index(values: list[int], *, width: int = 6) -> str:
    """
    int[width] 1-index 직렬화 — 인덱스 1..width, 값 공백 구분, 줄 끝 \\n.
    UnitConverter Logic: width=3 (meter/feet/yard 순) 또는 test 계약 width.
    """
    if len(values) != width:
        raise ValueError(f"expected {width} ints, got {len(values)}")
    # 1-index 라벨 + 값 (고정 포맷)
    lines = [f"{i}\t{v}" for i, v in enumerate(values, start=1)]
    return "\n".join(lines) + "\n"


def format_error_string(exc_type: str, message: str) -> str:
    """에러 코드 문자열 포맷 고정 — E001~E005 금지, ValueError 계약."""
    return f"{exc_type}: {message}\n"
```

### Step 2 — golden 연결

**경로 규칙:** `tests/golden/{id}.approved.txt`

| golden `{id}` | Test ID 예 | 내용 |
|---------------|-----------|------|
| `r1` | R1 | `convert_all` 직렬화 또는 `format_output` 줄 |
| `r2` | R2 | `to_meters` 결과 1줄 |
| `r4` | R4 | `format_error_string("ValueError", …)` |
| `r6` | R6 | `format_output` 줄 목록 (줄바꿈 `\n` 고정) |

test 끝에 hook (예 R2):

```python
from _approval import assert_matches_golden, format_error_string

def test_to_meters_feet_to_meter():
    # … Act …
    actual = f"{result:.6f}\n"  # 고정 소수 포맷
    assert_matches_golden(actual, "r2")
```

### Step 3 — 기준 파일 생성

```bash
# Windows PowerShell
$env:UPDATE_GOLDEN=1; python -m pytest tests/test_unit_converter.py::test_to_meters_feet_to_meter -v

# Windows cmd / macOS / Linux
UPDATE_GOLDEN=1 python -m pytest tests/test_unit_converter.py::test_to_meters_feet_to_meter -v
```

- 생성 파일: `tests/golden/r2.approved.txt`
- **Step 3 직후** golden 내용이 test 직렬화와 **동일**한지 눈으로 확인 (자동 diff는 Step 4).

### Step 4 — matched 확인

```bash
# UPDATE_GOLDEN unset / 0
python -m pytest tests/test_unit_converter.py::test_to_meters_feet_to_meter -v
```

- **PASS** = matched.
- **FAIL** `golden mismatch` → `src/` 또는 직렬화 수정 후 Step 3 **재실행** — golden 파일 **직접 편집 금지**.

## 5. 고정 직렬화 규칙

### 5.1 int[6] 1-index (공통 헬퍼)

| 규칙 | 내용 |
|------|------|
| 인덱스 | **1부터** (`1..width`, 기본 width=6) |
| 한 줄 | `{index}\t{value}` |
| 파일 끝 | 마지막 줄 `\n` |
| UnitConverter Logic | width=**3** — meter(1)·feet(2)·yard(3) 순 **또는** test 계약에 명시된 width |

```python
# convert_all → golden (Logic, width=3)
converted = convert_all("meter", 2.5)
ordered = [converted["meter"], converted["feet"], converted["yard"]]
# 반올림 PM 확정 전: test와 동일 precision만 사용
body = format_int_array_1_index([int(round(x * 100)) for x in ordered], width=3)
assert_matches_golden(body, "r1")
```

> width=6·1-index는 **공통 Approval 포맷**. UnitConverter는 **width=3** 또는 **텍스트 줄**(`format_output`) 중 test RED 계약에 맞는 쪽만 사용.

### 5.2 에러 코드 문자열 포맷 (고정)

| 규칙 | 내용 |
|------|------|
| 형식 | `{ExcType}: {message}\n` — `format_error_string` **필수** |
| 허용 | `ValueError: Invalid format…` · `ValueError: Unknown unit: cubit` |
| 금지 | `E001`~`E005` · dict status code · golden/actual **불일치 포맷** |

```python
with pytest.raises(ValueError) as exc_info:
    parse_input("invalid")
actual = format_error_string(type(exc_info.value).__name__, str(exc_info.value))
assert_matches_golden(actual, "r4")
```

### 5.3 golden 수동 편집 금지

| 허용 | 금지 |
|------|------|
| `UPDATE_GOLDEN=1` pytest로 **재생성** | `.approved.txt` 에디터 수정으로 FAIL → PASS |
| `src/`·직렬화 코드 수정 후 Step 3 재실행 | expected만 바꿔 diff 제거 |
| PM 확정 후 RED·GREEN·golden **순서**로 갱신 | assert 완화·`assert_matches_golden` 우회 |

## 6. 금지

| 금지 | 이유 |
|------|------|
| golden **수동** 편집으로 matched | Approval 우회 |
| `UPDATE_GOLDEN` 없이 golden 파일 **신규 작성** | Step 3 우회 |
| 이번 Test ID 외 golden 일괄 UPDATE | 1묶음 원칙 |
| assert·approx 완화 | RED/GREEN 계약 훼손 |
| E001~E005 in golden | 프로젝트 ECB |
| `[미결: PM]` test golden | PM 확정 전 |

## 7. 완료 보고

```markdown
Phase: green | Layer: entity | Track: Logic

## Golden Master 보고
| 항목 | 내용 |
|------|------|
| Test ID | R? |
| golden 경로 | `tests/golden/r?.approved.txt` |
| UPDATE_GOLDEN | Step 3 실행함 / 기준 신규 생성 |
| matched | YES — Step 4 PASS / NO — (diff 요약) |
| diff 요약 | (불일치 시) 1~3줄 또는 첫 diff hunk |
| 변경 파일 | `tests/_approval.py`, `tests/golden/…`, `tests/test_…` |
```

**diff 요약 예:**

```text
line 2: expected "1\t100" actual "1\t99"
```

**완료 한 줄 (matched YES일 때):**

```text
Golden Master 승인 완료 — 다음 RED 또는 REFACTOR 진행 가능
```

## 8. pytest 명령 요약

```bash
# Step 0 — PASS 전제
python -m pytest tests/test_unit_converter.py::test_to_meters_feet_to_meter -v

# Step 3 — 기준 생성
UPDATE_GOLDEN=1 python -m pytest tests/test_unit_converter.py::test_to_meters_feet_to_meter -v

# Step 4 — matched
python -m pytest tests/test_unit_converter.py::test_to_meters_feet_to_meter -v
```

PowerShell: `$env:UPDATE_GOLDEN=1; python -m pytest …`

## 9. 완료 체크

- [ ] 대상 Test ID pytest **PASS** (Step 0)
- [ ] `tests/_approval.py` · `assert_matches_golden` 존재
- [ ] `tests/golden/{id}.approved.txt` Step 3으로 생성
- [ ] Step 4 **UPDATE_GOLDEN 없이** PASS (matched)
- [ ] golden 수동 편집 없음
- [ ] int 1-index · 에러 문자열 **고정 포맷** 준수
- [ ] Golden Master 보고 (경로 · matched · diff)

## 10. 관련 Command

| Command | Phase | 산출 |
|---------|-------|------|
| `/green-minimal` | GREEN | `src/` PASS |
| `/golden-master` | GREEN+ | Approval snapshot |
| `/tdd-red` | RED | assert 계약 (golden 직렬화 SSOT) |

| 순서 | Command |
|------|---------|
| 1 | `/green-minimal` → PASS |
| 2 | `/golden-master` → matched |
| 3 | 다음 RED 또는 REFACTOR |
