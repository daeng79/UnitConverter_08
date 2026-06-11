# /red-test-plan — ARRR A단계 (Ask = RED ③) 테스트 플랜

C2C 설계표·테스트 플랜만 작성한다. **코드·테스트 파일을 생성·수정하지 않는다.**

후속: 설계 확정 후 `/red-skeleton` → `/tdd-red`(또는 skeleton 내 RED 작성) 순서.

## 1. 역할·범위

| 항목 | 내용 |
|------|------|
| ARRR | **A**sk — RED 사이클 ③ (설계·플랜) |
| 산출물 | 채팅 응답 4블록 (표) |
| 수정 허용 | **없음** — `tests/`·`src/`·기타 파일 생성·수정 금지 |
| Track A (boundary) | CLI·I/O 경계 (`UnitConverter.py`) — **Layer: boundary** 로만 변경하면 본 Command 재사용 |
| Track B (Logic) | 도메인 로직 (`src/unit_converter.py`) — 기본 **Layer: entity**, **Track: Logic** |

## 2. SSOT (읽기 전용)

우선순위 — `.cursorrules` · `doc/PRD.md` · 채팅 맥락:

1. PM 미결 확정값
2. 기존 RED 테스트·플랜 (채팅·`tests/` 현황)
3. `doc/PRD.md` — FR·R1~R6·API 계약
4. `report/02_workbook_scope_verification.md`
5. `README.md` · `UnitConverter.py` (baseline 참고)

> 사용자가 `@docs/PRD.md` 를 지정해도 저장 경로는 **`doc/PRD.md`** 를 SSOT로 본다.

## 3. 추가 입력 없이 동작

`/red-test-plan` **만** 입력해도 실행한다. 사용자에게 Test ID·주제를 묻지 않는다.

### 자동 추출 규칙

| 항목 | 추출 소스 | 규칙 |
|------|----------|------|
| **세션 주제** | 채팅 최근 맥락 → 없으면 PRD §3 제품 목표 | 한 줄 요약 |
| **Test ID** | PRD §9 R1~R6 · 채팅에서 지정된 ID · `tests/` 미작성 ID | **다음 1건** (이미 작성·플랜된 ID 제외) |
| **Layer / Track** | 대상 API·파일 | `src/unit_converter.py` → entity + Logic · `UnitConverter.py` → boundary + UI |
| **FR 인용** | PRD §6 FR-n | Test ID 시나리오에 매핑되는 FR 1개 |
| **[미결: PM]** | PRD §4.2 · `.cursorrules` incomplete | 해당 시 `# [미결: PM]` 표기 |

### Test ID ↔ FR ↔ API (UnitConverter 기본 매핑)

| Test ID | PRD FR | 대상 함수 | 시나리오 (요약) | 작성 상태 |
|---------|--------|----------|----------------|----------|
| R1 | FR-3 | `convert_all` | `meter:2.5` → feet/yard | PRD: 작성됨 |
| R2 | FR-2, FR-3 | `to_meters` / `convert_all` | `feet:3.28084` → meter ≈ 1, 교차 | 미작성 |
| R3 | FR-1 | `parse_input` | `meter:-2.5` 음수 정책 | 미작성 |
| R4 | FR-1 | `parse_input` | `invalid` 형식 오류 | 미작성 |
| R5 | FR-1 | `parse_input` | `cubit:1` 미지원 단위 | 미작성 |
| R6 | FR-4 | `format_output` | `meter:2.5` 출력 줄·포맷 | 미작성 |

플랜 대상이 **R1**이고 `tests/test_unit_converter.py`에 이미 존재하면 → **R2**부터 순차 선택.

## 4. Phase 선언 (필수)

응답 **첫 줄**에 반드시 선언 (`.cursorrules` `[Phase: RED]` 변형):

```text
Phase: red | Layer: entity | Track: Logic
```

| Layer | Track | 대상 |
|-------|-------|------|
| `entity` | `Logic` | `src/unit_converter.py` — parse / convert / format |
| `boundary` | `UI` | `UnitConverter.py` — 프롬프트·print·종료 코드 |

- `Phase: red` — 소문자 `red` (GREEN/REFACTOR 혼용 금지).
- Track A(boundary): **Layer만 `boundary`**, Track **`UI`** 로 바꾸면 동일 4블록·C2C 재사용.

## 5. 출력 4블록 (표 형식)

응답 본문은 아래 **4개 블록만** 순서대로 출력한다. 서술은 표 셀 안에 압축.

---

### 블록 1 — C2C (Rule1~3)

**C2C**: Contract → To-Do → Case (RED 1시나리오 = 1행)

| Rule | 열 | 내용 |
|------|-----|------|
| **Rule1** | PRD FR 인용 | `doc/PRD.md` §6 FR-n 원문 또는 요약 1문장 (§·항 번호 명시) |
| **Rule2** | To-Do 1개 | 이번 RED에서 검증할 행위 **1개** (동사 시작, 1시나리오) |
| **Rule3** | Test ID · G/W/T | **Given** / **When** / **Then** — Test ID 1개 |

**출력 표 템플릿:**

| Rule | PRD FR 인용 | To-Do (1개) | Test ID | Given | When | Then |
|------|-------------|-------------|---------|-------|------|------|
| Rule1~3 | (FR 인용) | (To-Do) | R? | (전제) | (함수 1회 호출) | (기대 결과 / ValueError) |

- PM 미결 항목: Then 또는 Given에 `[미결: PM]` 표기.
- Rule2는 Rule3 Test ID와 **1:1**.

---

### 블록 2 — Track B 표 (Logic) / Track A (boundary)

**Track B (Logic, Layer: entity)** — 도메인 RED 설계표:

| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|---------|----------|--------------|-----------|----------------------|
| R? | `parse_input` / `to_meters` / `convert_all` / `format_output` | Given … → Then … (한 셀) | 변환 불변식·에러 계약 (meter 경유, ValueError 등) | stub/미구현 시 pytest 실패 유형 1줄 |

**Track A (boundary, Layer: boundary)** — UI RED 설계표 (동일 열, 대상만 CLI):

| Test ID | 대상 | Given → Then | Invariant | Expected RED Failure |
|---------|------|--------------|-----------|---------------------|
| U? | `UnitConverter.main` / stdout | … | CLI 계약 (프롬프트·출력 줄) | … |

- 이번 Command 기본값: **Track B 1행** (다음 미작성 R?).
- boundary 플랜 시: Layer·Track만 바꾸고 **동일 4블록** 출력.

**Invariant 예시 (Logic):**

- meter 중간값 경유 (`METER_TO_FEET=3.28084`, `METER_TO_YARD=1.09361`)
- `convert_all` 키 = `{meter, feet, yard}`
- 형식·숫자·미지원 단위 → `ValueError`

**Expected RED Failure 예시:**

- `AttributeError` / `NotImplementedError` — stub `...`
- assertion FAIL — 기대값 vs 미구현
- incomplete — 정책 미정으로 Then·구현 불일치 (의도 FAIL)

---

### 블록 3 — 테스트 플랜

| 항목 | 값 |
|------|-----|
| **파일 경로** | `tests/test_unit_converter.py` (Logic) · boundary 시 `tests/test_unit_converter_cli.py` (플랜만, 미생성) |
| **함수명** | `test_<대상>_<시나리오>` (snake_case, 영어) |
| **conftest 픽스처** | 현재: **없음** (`tests/conftest.py` 미존재). 필요 시 `/red-skeleton`에서만 추가 — 본 Command에서 생성 금지 |
| **import** | `from unit_converter import <대상>` · `import pytest` |
| **AAA** | Arrange → Act (함수 **1개** 1회) → Assert (`pytest.raises` / `approx` / `==`) |
| **pytest 명령** | `python -m pytest tests/test_unit_converter.py::<함수명> -v` |
| **RED 묶음 범위** | **1 RED = 1 test 함수 = 1 Test ID** (R1~R6 중 1개; 다중 시나리오 뭉침 금지) |
| **SC-3 목표** | 전체 R1~R6 각 1 test (≥6) — 이번 플랜은 그중 **1건** |

PM 미결: Assert 블록에 `# [미결: PM]` 주석 **플랜에 명시** (코드 작성은 `/red-skeleton`·`/tdd-red`).

---

### 블록 4 — ECB · Mock 점검

| 점검 | Logic Track (entity) | boundary Track (UI) |
|------|---------------------|----------------------|
| **Domain Mock** | **금지** — `parse_input` / `convert_all` 등 **실제 호출** | CLI는 `capsys`/`monkeypatch`만 허용; **도메인 Mock 금지** |
| **E001~E005 emit** | **금지** — 테스트·플랜에 E001~E005 에러코드 emit·assert **넣지 않음** | 동일 |
| **ECB** | **E**rror(`ValueError` 계약) · **C**ontract(PRD FR) · **B**oundary(입력 문자열 경계) — **순수 함수 단위** | **B**oundary = stdin/stdout · **C**ontract = CLI 출력 형태 · **E**rror = 종료·메시지 |
| **skip / xfail** | **금지** — incomplete는 주석으로만 | 동일 |

Logic Track에서 `unittest.mock.patch`로 `convert_all` 등 도메인을 대체하는 플랜 → **블록 4에서 FAIL, 플랜 수정**.

## 6. 금지

| 금지 | 이유 |
|------|------|
| `src/` · `UnitConverter.py` 수정 | GREEN / 구현 Phase |
| `tests/` · `conftest.py` **생성·수정** | `/red-skeleton` · `/tdd-red` |
| GREEN / REFACTOR 선언·작업 | Phase: red 만 |
| `pytest.skip` · `pytest.mark.xfail` | incomplete는 `[미결: PM]` 주석 |
| assert 완화·다중 Test ID 1함수 | 1 RED = 1 시나리오 |
| E001~E005 emit | Logic/UI Track 공통 금지 |
| Domain Mock (Logic Track) | 순수 로직 계약 검증 |

## 7. 완료 조건

- [ ] 첫 줄 `Phase: red | Layer: … | Track: …`
- [ ] 추가 질문 없이 Test ID·주제 자동 추출
- [ ] 블록 1~4 표 **전부** 작성
- [ ] C2C Rule1~3 1행 = Test ID 1개
- [ ] 파일 생성·수정 **0건**

**완료 한 줄 (응답 마지막):**

```text
/red-skeleton 으로 넘길 준비됐다
```

## 8. 출력 예시 (R2 — Logic Track)

```markdown
Phase: red | Layer: entity | Track: Logic

## 블록 1 — C2C (Rule1~3)

| Rule | PRD FR 인용 | To-Do (1개) | Test ID | Given | When | Then |
|------|-------------|-------------|---------|-------|------|------|
| Rule1~3 | FR-2: 지원 단위 meter/feet/yard를 meter로 환산 (`to_meters`) | feet 3.28084 입력 시 meter ≈ 1.0 환산 검증 | R2 | unit=`feet`, value=`3.28084` | `to_meters("feet", 3.28084)` 호출 | 반환값 ≈ 1.0 (meter 경유) |

## 블록 2 — Track B

| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|---------|----------|--------------|-----------|----------------------|
| R2 | `to_meters` | Given feet·3.28084 → Then meter≈1.0 | `value / METER_TO_FEET`, METER_TO_FEET=3.28084 | stub `...` → 실행 불가 또는 assertion FAIL |

## 블록 3 — 테스트 플랜

| 항목 | 값 |
|------|-----|
| 파일 경로 | `tests/test_unit_converter.py` |
| 함수명 | `test_to_meters_feet_to_meter` |
| conftest 픽스처 | 없음 |
| pytest 명령 | `python -m pytest tests/test_unit_converter.py::test_to_meters_feet_to_meter -v` |
| RED 묶음 범위 | R2 단독 (1 함수 · 1 assert 블록) |

## 블록 4 — ECB · Mock 점검

| 점검 | 결과 |
|------|------|
| Domain Mock | 없음 ✓ |
| E001~E005 emit | 없음 ✓ |
| ECB | E: N/A · C: FR-2 · B: feet 단위 경계 |
| skip/xfail | 없음 ✓ |

/red-skeleton 으로 넘길 준비됐다
```

---

## 9. 관련 Command

| Command | Phase | 파일 |
|---------|-------|------|
| `/red-test-plan` | Ask (RED ③) | 생성 금지 — 플랜만 |
| `/red-skeleton` | RED ④ | 테스트 골격 생성 (후속) |
| `/tdd-red` | RED 실행 | `tests/` 실패 테스트 1건 추가 |
