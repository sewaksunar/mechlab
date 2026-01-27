from mechlab.units.registry import UNITS


class UnitError(Exception):
    pass


def find_category(unit: str) -> str:
    for category, units in UNITS.items():
        if unit in units:
            return category
    raise UnitError(f"Unknown unit: {unit}")


def convert(value: float, from_unit: str, to_unit: str) -> float:
    from_cat = find_category(from_unit)
    to_cat = find_category(to_unit)

    if from_cat != to_cat:
        raise UnitError(
            f"Incompatible units: {from_unit} → {to_unit}"
        )

    base_value = value * UNITS[from_cat][from_unit]
    return base_value / UNITS[to_cat][to_unit]
