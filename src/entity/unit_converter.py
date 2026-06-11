"""길이 단위 변환 — entity 핵심 API (GREEN 단계에서 구현)."""

from entity.constants import METER_TO_FEET, METER_TO_YARD


def parse_input(input_str: str) -> tuple[str, float]:
    if ":" not in input_str:
        raise ValueError("Invalid format. Use unit:value")
    unit, value_str = input_str.split(":", 1)
    try:
        value = float(value_str)
    except ValueError as exc:
        raise ValueError(f"Invalid number: {value_str}") from exc
    return unit, value


def to_meters(unit: str, value: float) -> float:
    if unit == "meter":
        return value
    if unit == "feet":
        return value / METER_TO_FEET
    ...


def convert_all(unit: str, value: float) -> dict[str, float]:
    meters = to_meters(unit, value)
    return {
        "meter": meters,
        "feet": round(meters * METER_TO_FEET, 1),
        "yard": round(meters * METER_TO_YARD, 1),
    }


def format_output(unit: str, value: float, converted: dict[str, float]) -> list[str]:
    ...
