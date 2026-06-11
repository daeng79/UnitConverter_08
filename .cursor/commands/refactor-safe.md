# /refactor-safe — ARRR Refine ⑧ Budget 내 리팩터

**선행**: `/refactor-smell` — pytest **전부 PASS** + P0 후보 1개 선택.

## Phase

```text
Phase: refactor | Scope: src/ | Track: Logic+UI
```

## Change Budget (1회)

| 항목 | 상한 |
|------|------|
| 파일 | ≤ 3 |
| 클래스 | ≤ 1 |
| 메서드 | ≤ 3 |
| 우선순위 | **P0 1개만** |

## 수정 허용

- `src/` (entity · control · boundary · shim)
- `UnitConverter.py` (boundary Track)
- **금지**: `tests/` assert·계약 변경, M2 OCP 전면 리팩

## 절차

1. `python -m pytest tests/ -v` — PASS 확인
2. smell 후보 1개·Budget 명시
3. 최소 diff 리팩터
4. `python -m pytest tests/ -v` — **전부 PASS**
5. git commit — 사용자 명시 요청 시만

## ECB 예 (P0)

- CLI 변환식 제거 → `entity.unit_converter` 위임
- Magic Number → `entity.constants` import

## 금지

- P0+P1 동시 1회 처리
- Budget 초과
- pytest FAIL 상태에서 진행

## 관련

| Command | 역할 |
|---------|------|
| `/refactor-smell` | 탐지만 (⑦) |
| **`/refactor-safe`** | 실행 (⑧) |
