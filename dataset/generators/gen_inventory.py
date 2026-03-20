# generators/gen_inventory.py
# Generates ~5,000 inventory records (product-warehouse-seller combinations)

import random
from datetime import datetime, timedelta

random.seed(42)


def generate_inventory(product_rows, warehouse_ids):
    """
    Generate inventory records.
    
    Each product is stocked in 1-4 warehouses.
    Inventory is tied to the product's seller.
    
    Args:
        product_rows: list of product tuples (from gen_products)
        warehouse_ids: list of warehouse_id strings
    """

    inventory = []
    inv_id = 0

    for product_tuple in product_rows:
        product_id = product_tuple[0]
        seller_id = product_tuple[1]

        # Each product in 1-4 warehouses (weighted toward 2-3)
        num_warehouses = random.choices([1, 2, 3, 4], weights=[0.20, 0.35, 0.30, 0.15], k=1)[0]
        selected_warehouses = random.sample(warehouse_ids, min(num_warehouses, len(warehouse_ids)))

        for wh_id in selected_warehouses:
            inv_id += 1
            inventory_id = f"INV{inv_id:06d}"

            # Available qty: 0-200 (weighted toward 10-50)
            available_qty = max(0, int(random.gauss(40, 25)))

            # Reserved qty: 0-10% of available
            reserved_qty = random.randint(0, max(1, available_qty // 10))

            # Damaged qty: 0-3% of available
            damaged_qty = random.randint(0, max(1, available_qty // 30))

            # Last updated: within last 30 days
            days_ago = random.randint(0, 30)
            last_updated = datetime.now() - timedelta(days=days_ago)

            inventory.append((
                inventory_id,
                product_id,
                seller_id,
                wh_id,
                available_qty,
                reserved_qty,
                damaged_qty,
                last_updated,
            ))

    return inventory


INVENTORY_COLUMNS = [
    "inventory_id", "product_id", "seller_id", "warehouse_id",
    "available_qty", "reserved_qty", "damaged_qty", "last_updated"
]