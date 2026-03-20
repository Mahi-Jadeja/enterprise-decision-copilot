# generators/gen_orders.py
# Generates ~8,000 orders and ~18,000 order items

import random
from datetime import date, timedelta
from helpers.constants import (
    ORDER_STATUSES, ORDER_STATUS_WEIGHTS,
    ORDER_CHANNELS, ORDER_CHANNEL_WEIGHTS,
    ORDER_PAYMENT_MODES, ORDER_PAYMENT_WEIGHTS,
)

random.seed(42)

NUM_ORDERS = 8000


def generate_orders_and_items(customer_ids, product_rows, seller_ids):
    """
    Generate orders and order_items together (they're tightly coupled).
    
    Args:
        customer_ids: list of customer_id strings
        product_rows: list of product tuples (product_id, seller_id, ..., selling_price is index 8)
        seller_ids: list of seller_id strings (not used directly, derived from products)
    
    Returns:
        (orders_list, order_items_list)
    """

    orders = []
    order_items = []
    item_counter = 0

    # Build a quick product lookup
    # product_rows: (product_id, seller_id, brand, category, sub_category, 
    #                size, color, mrp, selling_price, season, is_returnable)
    product_index = {p[0]: p for p in product_rows}
    product_ids = [p[0] for p in product_rows]

    for i in range(1, NUM_ORDERS + 1):
        order_id = f"ORD{i:06d}"

        customer_id = random.choice(customer_ids)

        # Order date: spread over last 18 months
        days_ago = random.randint(1, 540)
        order_date = date.today() - timedelta(days=days_ago)

        # Order status
        order_status = random.choices(
            ORDER_STATUSES, weights=ORDER_STATUS_WEIGHTS, k=1
        )[0]

        # Payment mode
        payment_mode = random.choices(
            ORDER_PAYMENT_MODES, weights=ORDER_PAYMENT_WEIGHTS, k=1
        )[0]

        # Order channel
        order_channel = random.choices(
            ORDER_CHANNELS, weights=ORDER_CHANNEL_WEIGHTS, k=1
        )[0]

        # Number of items: 1-3 (weighted)
        num_items = random.choices([1, 2, 3], weights=[0.50, 0.35, 0.15], k=1)[0]

        # Select products for this order (no duplicates)
        selected_products = random.sample(
            product_ids, min(num_items, len(product_ids))
        )

        total_amount = 0.0
        items_for_this_order = []

        for prod_id in selected_products:
            item_counter += 1
            order_item_id = f"OI{item_counter:07d}"

            product = product_index[prod_id]
            seller_id = product[1]
            selling_price = float(product[8])
            quantity = random.choices([1, 2], weights=[0.85, 0.15], k=1)[0]

            item_price = round(selling_price * quantity, 2)
            total_amount += item_price

            # Item status mirrors order status for most cases
            if order_status == "Delivered":
                item_status = "Delivered"
            elif order_status == "Cancelled":
                item_status = "Cancelled"
            elif order_status == "Shipped":
                item_status = "Shipped"
            else:
                item_status = "Processing"

            items_for_this_order.append((
                order_item_id,
                order_id,
                prod_id,
                seller_id,
                quantity,
                item_price,
                item_status,
            ))

        # Calculate order-level amounts
        total_amount = round(total_amount, 2)

        # Discount: 0-30% of total
        discount_pct = random.choices(
            [0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30],
            weights=[0.25, 0.15, 0.20, 0.15, 0.10, 0.10, 0.05],
            k=1
        )[0]
        discount_amount = round(total_amount * discount_pct, 2)
        final_payable = round(total_amount - discount_amount, 2)

        orders.append((
            order_id,
            customer_id,
            order_date,
            order_status,
            payment_mode,
            total_amount,
            discount_amount,
            final_payable,
            order_channel,
        ))

        order_items.extend(items_for_this_order)

    return orders, order_items


ORDERS_COLUMNS = [
    "order_id", "customer_id", "order_date", "order_status",
    "payment_mode", "total_amount", "discount_amount",
    "final_payable", "order_channel"
]

ORDER_ITEMS_COLUMNS = [
    "order_item_id", "order_id", "product_id", "seller_id",
    "quantity", "item_price", "item_status"
]