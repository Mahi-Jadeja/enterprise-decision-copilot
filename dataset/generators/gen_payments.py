# generators/gen_payments.py
# Generates one payment record per order (~8,000 rows)

import random
from datetime import datetime, timedelta
from helpers.constants import (
    PAYMENT_METHODS_PREPAID, PAYMENT_GATEWAYS,
)

random.seed(42)


def generate_payments(order_rows):
    """
    Generate one payment per order.
    
    Args:
        order_rows: list of order tuples
            (order_id, customer_id, order_date, order_status, 
             payment_mode, total_amount, discount_amount, 
             final_payable, order_channel)
    """

    payments = []

    for i, order in enumerate(order_rows, 1):
        payment_id = f"PAY{i:06d}"

        order_id = order[0]
        order_date = order[2]  # date object
        order_status = order[3]
        payment_mode = order[4]  # COD or Prepaid
        final_payable = float(order[7])

        # Payment method
        if payment_mode == "COD":
            payment_method = "COD"
        else:
            payment_method = random.choice(PAYMENT_METHODS_PREPAID)

        # Payment status
        if order_status == "Cancelled":
            payment_status = "Failed"
        elif order_status == "Delivered":
            payment_status = "Completed"
        elif payment_mode == "COD" and order_status in ("Shipped", "Processing"):
            payment_status = "Pending"
        else:
            payment_status = "Completed"

        # Payment date: same day or +1 day from order
        if isinstance(order_date, datetime):
            payment_date = order_date + timedelta(hours=random.randint(0, 12))
        else:
            payment_date = datetime.combine(
                order_date, datetime.min.time()
            ) + timedelta(hours=random.randint(0, 12))

        # Paid amount
        if payment_status == "Failed":
            paid_amount = 0.0
        else:
            paid_amount = final_payable

        # Gateway
        if payment_method == "COD":
            gateway = "COD"
        else:
            gateway = random.choice(PAYMENT_GATEWAYS)

        payments.append((
            payment_id,
            order_id,
            payment_method,
            payment_status,
            payment_date,
            paid_amount,
            gateway,
        ))

    return payments


PAYMENTS_COLUMNS = [
    "payment_id", "order_id", "payment_method", "payment_status",
    "payment_date", "paid_amount", "gateway"
]