# /refactor-smell — ARRR R단계 (Refine ⑦) 코드 스멜 탐지

**탐지만** 수행한다. 코드·테스트 **수정 금지**, **commit 금지**.  
후속 수정은 **`/refactor-safe`** (Change Budget 내).

**프로젝트:** UnitConverter_08 — `src/` (Logic) · `UnitConverter.py` (UI) · `tests/`

## 1. 역할·범위

| 항목 | 내용 |
|------|------|
| ARRR | **R**efine — 사이클 **⑦** (스멜 분석) |
| 선행 | GREEN·golden(선택) 완료 · **전체 pytest PASS** |
| 후속 | `/refactor-safe` — **P0 1개**만 골라 실행 |
| 산출물 | 스멜 표 + `/refactor-safe` 후보 1~3개 (채팅 응답) |
| 수정 허용 | **없음** |

| Track | Scope | 점검 대상 |
|-------|-------|----------|
| Logic | `src/` | `constants.py` · `unit_converter.py` |
| UI | `UnitConverter.py` | CLI · print · 입력 루프 |
| tests | `tests/` | 중복 Arrange · 헬퍼 부재 (구조만, assert 변경 제안 금지) |

## 2. 전제 — pytest 전부 PASS

```bash
python -m pytest tests/ -v
```

| 결과 | 동작 |
|------|------|
| **전부 PASS** | 스멜 탐지 **진행** |
| **1건이라도 FAIL** | **즉시 중단** — 스멜 표 작성 금지. FAIL test·원인 한 줄 보고 후 GREEN/fix 먼저 |
| 미실행 | Command 실행 전 **반드시** pytest 실행 |

추가 입력 없이 `/refactor-smell` 만으로 동작. pytest는 **실제 실행** 후 결과를 근거로 보고.

## 3. Phase 선언 (필수)

응답 **첫 줄**:

```text
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI
```

- `Phase: refactor` — GREEN/RED 혼용 금지.
- 본 Command는 **분석만** — `[Phase: REFACTOR]` 구현 Phase와 구분.

## 4. 스멜 유형 · 우선순위

| 유형 | 설명 | UnitConverter 흔적 |
|------|------|-------------------|
| **Long Method** | 한 함수가 파싱·변환·출력·검증 다수 담당 | `UnitConverter.main` 36줄 일체형 |
| **Duplicated Code** | 동일 변환식·if/elif 단위 분기 반복 | `3.28084` / `1.09361` in CLI vs `src/` |
| **Mysterious Name** | `meter_value`, `in_meters` 등 의도 불명 | baseline 변수명 |
| **Magic Number** | `constants.py` 우회 리터럴 | CLI 하드코딩 비율 |
| **ECB 위반** | entity → boundary import · control 혼재 | `unit_converter`가 print/input 참조 · CLI에 변환 로직 |
| **Feature Envy** | 타 모듈 데이터·상수에 과 의존 | CLI가 변환 알고리즘 전부 소유 |

### P0 / P1 / P2

| 등급 | 기준 | 예 |
|------|------|-----|
| **P0** | 테스트 PASS 유지 위험 · ECB·SSOT 위반 · 중복이 버그 유발 | Magic Number in CLI + Duplicated Code · ECB (변환 in CLI) |
| **P1** | 유지보수·확장 비용 · M1 범위 내 개선 | Long Method in `main` · Mysterious Name |
| **P2** | 미미 · M2/OCP 전 | tests Arrange 중복 · 네이밍 취향 |

## 5. Change Budget (`/refactor-safe` 전달용)

한 번의 `/refactor-safe` 실행 상한 — **스멜 보고에 명시**:

| 항목 | 상한 |
|------|------|
| **파일** | ≤ 3 |
| **클래스** | ≤ 1 |
| **메서드** | ≤ 3 |

후보 1~3개는 **각각** 이 Budget으로 **실행 가능한** 한 덩어리로 쪼갠다.

## 6. 절차

| Step | 작업 |
|------|------|
| 1 | `python -m pytest tests/ -v` — FAIL이면 **중단** |
| 2 | `src/` · `UnitConverter.py` · `tests/` **읽기만** — 스멜 수집 |
| 3 | 스멜 표 작성 (P0/P1/P2 · 유형 · 위치 · 근거 1줄) |
| 4 | `/refactor-safe` 후보 **1~3개** — Budget·Track·예상 파일 수 |
| 5 | **코드 수정 0건** · commit 없음 |

## 7. 출력 형식

응답 본문: **스멜 표** + **후보 표** + **다음 안내**.

### 7.1 스멜 표

| ID | P | 유형 | 위치 | 근거 (1줄) |
|----|---|------|------|------------|
| S1 | P0 | Magic Number | `UnitConverter.py` L19-21 | `3.28084`/`1.09361` — `constants.py` SSOT 미사용 |
| S2 | P0 | ECB 위반 | `UnitConverter.py` | boundary에 entity 변환 로직 · `src/unit_converter` 미연동 |
| … | … | … | … | … |

- **P** = P0 / P1 / P2
- **유형** = Long Method · Duplicated Code · Mysterious Name · Magic Number · ECB 위반 · Feature Envy (해당만)

### 7.2 `/refactor-safe` 후보 (1~3개)

| 후보 | 우선 P | 스멜 ID | Track | 예상 변경 | Budget |
|------|--------|---------|-------|----------|--------|
| C1 | P0 | S1,S2 | UI+Logic | CLI→`unit_converter` 위임, 상수 import | 파일 2 · 메서드 2 |
| C2 | P1 | S3 | UI | `main` 분리 (parse / print) | 파일 1 · 메서드 3 |
| … | … | … | … | … | 파일≤3 · 클래스≤1 · 메서드≤3 |

### 7.3 다음 안내 (필수)

```markdown
## 다음 단계
- **P0 1개만** 골라 `/refactor-safe` 실행 (예: 후보 C1).
- 본 Command에서는 수정·commit 하지 않음.
```

**완료 한 줄 (응답 마지막):**

```text
/refactor-safe — P0 후보 1개 선택 후 실행
```

## 8. 금지

| 금지 | 이유 |
|------|------|
| `src/` · `tests/` · `UnitConverter.py` **수정** | Refine ⑦ = 탐지만 |
| `git commit` · push | 사용자 요청·`/refactor-safe`까지 보류 |
| pytest FAIL 상태에서 스멜 표 | 전제 위반 |
| assert·golden·RED 계약 변경 제안을 **즉시 적용** | 별도 Phase |
| M2 전면 OCP 리팩 (범위 외) | `.cursorrules` OUT |
| 후보 4개 이상 | 집중력 — **1~3개** |
| P0·P1 동시 `/refactor-safe` 1회에 몰아넣기 | **P0 1개**만 |

## 9. 완료 보고 (pytest 선행)

```markdown
Phase: refactor | Scope: src/ tests/ | Track: Logic+UI

## pytest 전제
| 항목 | 내용 |
|------|------|
| 명령 | `python -m pytest tests/ -v` |
| 결과 | N passed — 진행 / FAIL — 중단 |

## 스멜 요약
| P0 | P1 | P2 |
|----|----|-----|
| n | n | n |

(스멜 표 · 후보 표 · 다음 안내)
```

## 10. 완료 체크

- [ ] `python -m pytest tests/ -v` **전부 PASS** (또는 FAIL 시 중단 보고만)
- [ ] 첫 줄 `Phase: refactor | Scope: src/ tests/ | Track: Logic+UI`
- [ ] 스멜 표 — P0/P1/P2 · 6유형 · 위치·근거
- [ ] `/refactor-safe` 후보 **1~3개** + Change Budget
- [ ] P0 **1개**만 `/refactor-safe` 안내
- [ ] 코드 수정 **0건** · commit **0건**

## 11. 관련 Command

| Command | Phase | 산출 |
|---------|-------|------|
| `/green-minimal` | GREEN | PASS |
| `/golden-master` | GREEN+ | Approval |
| `/refactor-smell` | Refine **⑦** | 스멜 표 (수정 없음) |
| `/refactor-safe` | Refine **⑧** | Budget 내 리팩터 + pytest PASS |

| 순서 | Command |
|------|---------|
| 1 | `/refactor-smell` — 탐지 |
| 2 | P0 후보 1개 선택 |
| 3 | `/refactor-safe` — 실행 |
