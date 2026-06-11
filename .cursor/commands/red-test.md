# /red-test — RED ⑤ assert RED (`/tdd-red` 별칭)

**`/tdd-red`와 동일** — `pytest.fail` 스켈레톤을 assert·도메인 호출 RED로 교체한다.

## Phase

```text
[Phase: RED]
```

또는 ARRR Track:

```text
Phase: red | Layer: entity | Track: Logic
```

## 수정

- **허용**: `tests/` — `from unit_converter import …` + assert / `pytest.raises`
- **금지**: `src/` · `UnitConverter.py`

## 선행·후속

| 순서 | Command |
|------|---------|
| ③ | `/red-test-plan` |
| ④ | `/red-skeleton` |
| **⑤** | **`/red-test`** (본 Command) = `/tdd-red` |
| GREEN | `/green-minimal` |

상세 규칙 → `.cursor/commands/tdd-red.md`
