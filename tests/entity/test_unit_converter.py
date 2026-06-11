import pytest
from unit_converter import convert_all, parse_input


def test_convert_all_meter_to_feet_and_yard():
    # Given — unit=meter, value=2.5
    # [확정: PM] 반올림 — README 예시 소수 1자리 (feet ≈ 8.2, yard ≈ 2.7, abs=0.05)
    unit, value = "meter", 2.5
    # When — convert_all(unit, value) → feet ≈ 8.2, yard ≈ 2.7
    result = convert_all(unit, value)
    # Then
    assert result["feet"] == pytest.approx(8.2, abs=0.05)
    assert result["yard"] == pytest.approx(2.7, abs=0.05)


def test_convert_all_feet_to_meter_and_cross():
    # Given — unit=feet, value=3.28084 (1 meter = 3.28084 feet)
    unit, value = "feet", 3.28084
    # When — convert_all(unit, value) → meter ≈ 1.0, yard 교차 변환
    result = convert_all(unit, value)
    # Then — meter 경유 역·교차 변환 (소수 1자리 반올림)
    assert result["meter"] == pytest.approx(1.0)
    assert result["yard"] == pytest.approx(1.1, abs=0.05)


def test_parse_input_negative_meter_policy():
    # Given — raw="meter:-2.5"
    # [확정: PM] 음수 입력 — 허용 (baseline 동작)
    raw = "meter:-2.5"
    # When — parse_input(raw) → ("meter", -2.5)
    unit, value = parse_input(raw)
    # Then
    assert unit == "meter"
    assert value == pytest.approx(-2.5)
