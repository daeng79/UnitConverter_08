---
name: pytest-boundary-test
description: UnitConverter CLI boundary 테스트 작성·실행 가이드. tests/boundary/, capsys, main() RED/GREEN 시 사용.
---

# pytest-boundary-test

CLI(boundary) Track 테스트 작성 시 따른다.

## 대상

- `UnitConverter.py` — `main()` 진입점
- `tests/boundary/test_unit_converter_cli.py` (플랜에 따라 생성)

## RED 규칙

- Logic Track과 동일: RED 1회 = test 1개 · 시나리오 1개
- entity 구현 전: `/red-skeleton` → `/tdd-red` 순서
- `capsys` 또는 `monkeypatch`로 stdin/stdout 검증

## 예시 (스켈레톤)

```python
import pytest


def test_cli_meter_input_prints_conversions(capsys, monkeypatch):
    # Given — stdin "meter:2.5"
    monkeypatch.setattr("builtins.input", lambda _: "meter:2.5")
    # When — main()
    # Then
    pytest.fail("RED: U1 — CLI meter:2.5 output lines [미결: PM]")
```

## 금지

- boundary 테스트에서 변환식 직접 assert (entity 책임)
- PM 미결(출력 줄 수·반올림) 추측 기대값

## 선행

- entity GREEN 완료 권장 (CLI는 entity 위임 후 테스트)

## 실행

```bash
python -m pytest tests/boundary/ -v
```
