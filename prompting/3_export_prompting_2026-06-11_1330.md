# Export Prompting — UnitConverter_08 세션 (README·명칭·RED 플랜)

## 메타정보

| 항목 | 내용 |
|------|------|
| Prefix | `3` |
| Export 시각 | 2026-06-11 13:30 |
| 총 사용자 프롬프트 | 4개 |
| 선행 export | `prompting/2_export_prompting_2026-06-11_1305.md` (문서·Command) |

---

## 프롬프트 목록 (시간순)

### [1] 사용자 프롬프트

> /red-test-plan
> Phase: red | Layer: entity | Track: Logic
> 이번 RED 묶음: D-LOC-01 (FR-LOC-01)
> 다음을 표로 작성해줘. tests/·src/ 파일은 만들지 마.
> 1. C2C 추적 (Rule 1~3 적용)
>    - PRD FR-LOC-01 인용 (docs/PRD.md)
>    - To-Do 1개 (판단 포함 항목만)
>    - Test ID → Given / When / Then
> 2. Track B (D-*) RED 설계표
>    | Test ID | 대상 함수 | Given→Then | Invariant | Expected RED Failure |
> 3. 테스트 플랜
>    - 파일: tests/entity/test_d_loc_01.py
>    - test 함수명 후보
>    - conftest 픽스처 (G1 격자 등, 로직 없음)
>    - pytest 명령:
>      python -m pytest tests/entity/test_d_loc_01.py::test_d_loc_01_blank_coords_row_major -v
>    - RED 묶음 범위 (이번 1~3 ID)
> 4. ECB·Mock 점검
>    - Logic Track → Domain Mock 금지
>    - entity E001~E005 emit 금지
> 금지: src/ 수정, GREEN/REFACTOR, skip/xfail
> 완료 후: /red-skeleton 으로 넘길 준비됐다고 한 줄로 알려줘.

**맥락/의도:** RED ③ C2C·테스트 플랜 4블록 — Grid 스타일 D-LOC 묶음 지정 (파일 생성 금지)

---

### [2] 사용자 프롬프트

> @README.md 파일 업데이트 해줘

**맥락/의도:** `doc/PRD.md`·현재 진행 상태에 맞게 README 갱신

---

### [3] 사용자 프롬프트

> 프로젝트명은 local 은 UnitConverter_09 이지만 GitHub, 문서등에는 UnitConverter_08 로 유지해라

**맥락/의도:** 공식 저장소·문서 명칭 08 고정, 로컬 폴더명과 분리

---

### [4] 사용자 프롬프트

> /export

**맥락/의도:** 본 세션 report·prompting export (prefix 3)

---

## 재사용 가능한 프롬프트 패턴

### 패턴 1: 커스텀 RED 묶음 + `/red-test-plan`

```
/red-test-plan
Phase: red | Layer: entity | Track: Logic
이번 RED 묶음: {묶음명} ({FR-ID})
(블록 1~4 지시 · tests/·src/ 생성 금지)
완료 후: /red-skeleton 으로 넘길 준비됐다
```

→ SSOT(`doc/PRD.md`)와 불일치 시 R1~R6·UnitConverter API로 매핑해 플랜만 산출

### 패턴 2: PRD 정합 README 갱신

```
@README.md 파일 업데이트 해줘
```

→ PRD·Command·테스트 현황·ARRR 파이프라인 반영

### 패턴 3: 로컬 vs 공식 프로젝트명 분리

```
프로젝트명은 local 은 {로컬폴더} 이지만 GitHub, 문서등에는 {공식명} 로 유지해라
```

→ README·`.cursorrules`·Command 메타에 공식명 규칙 고정

### 패턴 4: 세션 마감 export

```
/export
```

→ `report/`, `prompting/` prefix 순차 저장
