# generators/gen_returns.py
# Generates ~2,500 returns from delivered order items

import random
from datetime import timedelta
from helpers.constants import (
    RETURN_REASONS, RETURN_TYPES, RETURN_TYPE_WEIGHTS,
    RETURN_STATUSES, RETURN_RATE_BY_CATEGORY,
)

random.seed(42)


def generate_returns(order_items, order_lookup, product_lookup, seller_lookup):
    """
    Generate returns for delivered items based on category return rates.
    
    Args:
        order_items: list of order_item tuples
            (order_item_id, order_id, product_id, seller_id, quantity, item_price, item_status)
        order_lookup: dict {order_id: order_tuple} for getting order_date
        product_lookup: dict {product_id: product_tuple} for getting category
        seller_lookup: dict {seller_id: seller_tuple} for risk_flag
    
    Returns:
        list of return tuples
    """

    returns = []
    return_counter = 0

    # Filter to delivered items only
    delivered_items = [oi for oi in order_items if oi[6] == "Delivered"]

    for oi in delivered_items:
        order_item_id = oi[0]
        order_id = oi[1]
        product_id = oi[2]
        seller_id = oi[3]
        item_price = float(oi[5])

        # Get product category
        product = product_lookup.get(product_id)
        if not product:
            continue
        category = product[3]  # index 3 = category
        is_returnable = product[10]  # index 10 = is_returnable

        if not is_returnable:
            continue

        # Base return rate by category
        base_rate = RETURN_RATE_BY_CATEGORY.get(category, 0.20)

        # High-risk sellers have 1.5x return rate
        seller = seller_lookup.get(seller_id)
        if seller:
            risk_flag = seller[7]  # index 7 = risk_flag
            if risk_flag == "High":
                base_rate *= 1.5
            elif risk_flag == "Medium":
                base_rate *= 1.2

        # Decide if this item is returned
        if random.random() > base_rate:
            continue

        return_counter += 1
        return_id = f"RET{return_counter:06d}"

        # Return date: 2-15 days after order date
        order = order_lookup.get(order_id)
        if order:
            order_date = order[2]  # index 2 = order_date
            return_date = order_date + timedelta(days=random.randint(2, 15))
        else:
            continue

        return_reason = random.choice(RETURN_REASONS)

        return_type = random.choices(
            RETURN_TYPES, weights=RETURN_TYPE_WEIGHTS, k=1
        )[0]

        # Return status (weighted toward completion)
        return_status = random.choices(
            RETURN_STATUSES,
            weights=[0.05, 0.10, 0.10, 0.65, 0.10],
            k=1
        )[0]

        # Pickup date: 1-5 days after return initiation
        if return_status in ("Picked Up", "Received", "Completed"):
            pickup_date = return_date + timedelta(days=random.randint(1, 5))
        else:
            pickup_date = None

        # Refund amount: full or partial
        if return_type == "Exchange":
            refund_amount = 0.0
        else:
            # 80% get full refund, 20% get partial (90-100%)
            if random.random() < 0.80:
                refund_amount = item_price
            else:
                refund_amount = round(item_price * random.uniform(0.90, 1.0), 2)

        returns.append((
            return_id,
            order_item_id,
            return_date,
            return_reason,
            return_type,
            return_status,
            pickup_date,
            refund_amount,
        ))

    return returns


RETURNS_COLUMNS = [
    "return_id", "order_item_id", "return_date", "return_reason",
    "return_type", "return_status", "pickup_date", "refund_amount"
]