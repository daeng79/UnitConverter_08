def parse_input(input_str: str) -> tuple[str, float]:
    ...


def to_meters(unit: str, value: float) -> float:
    ...


def convert_all(unit: str, value: float) -> dict[str, float]:
    ...


def format_output(unit: str, value: float, converted: dict[str, float]) -> list[str]:
    ...
