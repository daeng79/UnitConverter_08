---
name: golden-master
description: UnitConverter baseline CLI 출력 golden master 비교. GREEN 후 Approval·회귀 검증 시 사용.
---

# golden-master

baseline `UnitConverter.py` 또는 GREEN 후 CLI 출력을 golden 파일과 비교한다.

## 사용 시점

- entity GREEN + CLI 연동 후
- REFACTOR 전후 회귀 확인 (선택)
- `/golden-master` command와 연동

## 절차

1. `python -m pytest tests/ -v` — **전부 PASS** 확인
2. 고정 입력(예: `meter:2.5`)으로 CLI 실행, stdout 캡처
3. PM 확정 전: `[미결: PM]` 출력 형태 — golden은 **확정 후**만 고정

## 저장 위치 (권장)

```
tests/boundary/golden/
  meter_2_5.txt
```

## 비교

```python
def test_cli_golden_meter(capsys, monkeypatch):
    golden = (Path(__file__).parent / "golden" / "meter_2_5.txt").read_text()
    monkeypatch.setattr("builtins.input", lambda _: "meter:2.5")
    from UnitConverter import main
    main()
    assert capsys.readouterr().out == golden
```

## 금지

- PM 미결(2줄 vs 3줄·반올림) 확정 전 golden 고정
- golden 실패 시 assert 삭제 — 원인 조사 후 PM 확인

## Command

`.cursor/commands/golden-master.md`
