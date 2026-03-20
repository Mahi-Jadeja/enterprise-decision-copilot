# generators/gen_seller_settlements.py
# Generates one settlement per delivered order item (~12,000 rows)

import random
from datetime import timedelta
from helpers.constants import (
    SETTLEMENT_STATUSES, SETTLEMENT_STATUS_WEIGHTS,
)

random.seed(42)


def generate_seller_settlements(order_items, order_lookup, seller_lookup):
    """
    Generate settlement records for delivered order items.
    
    Args:
        order_items: list of order_item tuples
        order_lookup: dict {order_id: order_tuple}
        seller_lookup: dict {seller_id: seller_tuple}
            seller_tuple index 6 = commission_rate
    """

    settlements = []
    settle_counter = 0

    for oi in order_items:
        order_item_id = oi[0]
        order_id = oi[1]
        seller_id = oi[3]
        item_price = float(oi[5])
        item_status = oi[6]

        # Only settle delivered items
        if item_status != "Delivered":
            continue

        settle_counter += 1
        settlement_id = f"SETT{settle_counter:06d}"

        # Get commission rate from seller
        seller = seller_lookup.get(seller_id)
        if seller:
            commission_rate = float(seller[6]) / 100.0  # index 6 = commission_rate
        else:
            commission_rate = 0.15  # fallback

        gross_amount = item_price
        commission_amount = round(gross_amount * commission_rate, 2)
        net_payable = round(gross_amount - commission_amount, 2)

        # Settlement date: 7-21 days after order date
        order = order_lookup.get(order_id)
        if order:
            order_date = order[2]
            settlement_date = order_date + timedelta(days=random.randint(7, 21))
        else:
            continue

        settlement_status = random.choices(
            SETTLEMENT_STATUSES, weights=SETTLEMENT_STATUS_WEIGHTS, k=1
        )[0]

        settlements.append((
            settlement_id,
            seller_id,
            order_item_id,
            gross_amount,
            commission_amount,
            net_payable,
            settlement_date,
            settlement_status,
        ))

    return settlements


SELLER_SETTLEMENTS_COLUMNS = [
    "settlement_id", "seller_id", "order_item_id",
    "gross_amount", "commission_amount", "net_payable",
    "settlement_date", "settlement_status"
]