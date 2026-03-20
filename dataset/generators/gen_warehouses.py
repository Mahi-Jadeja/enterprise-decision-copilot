# generators/gen_warehouses.py
# Generates exactly 10 warehouse records

from helpers.constants import WAREHOUSE_LOCATIONS


def generate_warehouses():
    """Generate warehouse tuples from predefined locations."""

    warehouses = []

    for i, (city, state, wh_type) in enumerate(WAREHOUSE_LOCATIONS, 1):
        warehouse_id = f"WH{i:03d}"
        is_active = True  # All warehouses active initially

        warehouses.append((
            warehouse_id,
            city,
            state,
            wh_type,
            is_active,
        ))

    return warehouses


WAREHOUSES_COLUMNS = [
    "warehouse_id", "warehouse_city", "warehouse_state",
    "warehouse_type", "is_active"
]