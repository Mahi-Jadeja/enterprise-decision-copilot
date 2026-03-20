# generators/gen_refunds.py
# Generates one refund per completed return (where refund_amount > 0)

import random
from datetime import timedelta

random.seed(42)

REFUND_METHODS = ["Original Payment Method", "Myntra Credit", "Bank Transfer"]
REFUND_METHOD_WEIGHTS = [0.50, 0.30, 0.20]


def generate_refunds(return_rows):
    """
    Generate refunds for returns that have refund_amount > 0 and status is Completed.
    
    Args:
        return_rows: list of return tuples
            (return_id, order_item_id, return_date, return_reason,
             return_type, return_status, pickup_date, refund_amount)
    """

    refunds = []
    refund_counter = 0

    for ret in return_rows:
        return_id = ret[0]
        return_date = ret[2]
        return_status = ret[5]
        refund_amount = float(ret[7])

        # Only create refund for completed returns with refund amount
        if return_status != "Completed" or refund_amount <= 0:
            continue

        refund_counter += 1
        refund_id = f"REF{refund_counter:06d}"

        refund_method = random.choices(
            REFUND_METHODS, weights=REFUND_METHOD_WEIGHTS, k=1
        )[0]

        # Refund processed 2-7 days after return date
        refund_date = return_date + timedelta(days=random.randint(2, 7))

        # 95% of refunds complete successfully
        refund_status = random.choices(
            ["Completed", "Processing", "Failed"],
            weights=[0.90, 0.07, 0.03],
            k=1
        )[0]

        if refund_status == "Failed":
            refunded_amount = 0.0
        else:
            refunded_amount = refund_amount

        refunds.append((
            refund_id,
            return_id,
            refund_method,
            refund_status,
            refund_date,
            refunded_amount,
        ))

    return refunds


REFUNDS_COLUMNS = [
    "refund_id", "return_id", "refund_method", "refund_status",
    "refund_date", "refunded_amount"
]