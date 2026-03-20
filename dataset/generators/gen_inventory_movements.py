# generators/gen_inventory_movements.py
# Generates ~25,000 inventory movement records

import random
from datetime import datetime, timedelta

random.seed(42)


def generate_inventory_movements(inventory_rows, order_items, return_rows):
    """
    Generate inventory movements that reference orders and returns.
    
    Movement types:
        - INBOUND: initial stock / restocking
        - OUTBOUND: order fulfillment
        - RETURN_INBOUND: returned items back to warehouse
        - ADJUSTMENT: damaged/lost stock corrections
    
    Args:
        inventory_rows: list of inventory tuples (for inventory_id references)
        order_items: list of order_item tuples (for OUTBOUND movements)
        return_rows: list of return tuples (for RETURN_INBOUND movements)
    """

    movements = []
    move_counter = 0

    inventory_ids = [inv[0] for inv in inventory_rows]

    # Map product_id -> list of inventory_ids
    product_to_inv = {}
    for inv in inventory_rows:
        pid = inv[1]  # product_id
        if pid not in product_to_inv:
            product_to_inv[pid] = []
        product_to_inv[pid].append(inv[0])

    # 1. INBOUND movements — initial stock for each inventory record
    for inv in inventory_rows:
        move_counter += 1
        movement_id = f"MOV{move_counter:07d}"
        inventory_id = inv[0]
        available_qty = inv[4]

        # Initial stock is roughly available + some buffer
        quantity = available_qty + random.randint(5, 50)
        movement_date = datetime.now() - timedelta(days=random.randint(60, 365))

        movements.append((
            movement_id,
            inventory_id,
            "INBOUND",
            quantity,
            "INITIAL_STOCK",
            movement_date,
        ))

    # 2. OUTBOUND movements — one per order item (map to an inventory record)
    for oi in order_items:
        product_id = oi[2]
        quantity = oi[4]
        order_item_id = oi[0]

        inv_ids = product_to_inv.get(product_id, [])
        if not inv_ids:
            continue

        move_counter += 1
        movement_id = f"MOV{move_counter:07d}"
        inventory_id = random.choice(inv_ids)

        movement_date = datetime.now() - timedelta(days=random.randint(1, 540))

        movements.append((
            movement_id,
            inventory_id,
            "OUTBOUND",
            quantity,
            order_item_id,
            movement_date,
        ))

    # 3. RETURN_INBOUND — one per return
    for ret in return_rows:
        return_id = ret[0]
        order_item_id = ret[1]
        return_status = ret[5]

        # Only if return is received/completed
        if return_status not in ("Received", "Completed"):
            continue

        # Find which product this return is for
        # We need order_item -> product mapping
        # For simplicity, pick a random inventory id
        # (In production you'd trace back properly)
        if not inventory_ids:
            continue

        move_counter += 1
        movement_id = f"MOV{move_counter:07d}"
        inventory_id = random.choice(inventory_ids)

        movement_date = datetime.now() - timedelta(days=random.randint(1, 200))

        movements.append((
            movement_id,
            inventory_id,
            "RETURN_INBOUND",
            1,  # typically 1 item returned
            return_id,
            movement_date,
        ))

    # 4. ADJUSTMENT movements — ~500 random adjustments
    for _ in range(500):
        move_counter += 1
        movement_id = f"MOV{move_counter:07d}"
        inventory_id = random.choice(inventory_ids)

        quantity = random.randint(-5, -1)  # negative = loss/damage
        movement_date = datetime.now() - timedelta(days=random.randint(1, 300))

        movements.append((
            movement_id,
            inventory_id,
            "ADJUSTMENT",
            quantity,
            "DAMAGE_AUDIT",
            movement_date,
        ))

    return movements


INVENTORY_MOVEMENTS_COLUMNS = [
    "movement_id", "inventory_id", "movement_type",
    "quantity", "reference_id", "movement_date"
]