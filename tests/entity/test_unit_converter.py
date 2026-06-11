import pytest

from unit_converter import convert_all, format_output, parse_input, to_meters


def test_convert_all_meter_to_feet_and_yard():
    # Arrange
    unit, value = "meter", 2.5
    # [미결: PM] 반올림 규칙 확정 전 — README 예시 8.2 / 2.7 기준

    # Act
    result = convert_all(unit, value)

    # Assert
    assert result["feet"] == pytest.approx(8.2, abs=0.05)
    assert result["yard"] == pytest.approx(2.7, abs=0.05)


def test_to_meters_feet_to_meter():
    # Given — unit=feet, value=3.28084 (1 meter = 3.28084 feet)
    unit, value = "feet", 3.28084
    # When — to_meters(unit, value) → meter ≈ 1.0
    # Then — 스켈레톤 RED (/tdd-red에서 assert·import 교체)
    pytest.fail("RED: R2 — to_meters(feet, 3.28084) ≈ 1.0 meter")
