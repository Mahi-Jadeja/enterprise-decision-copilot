# generators/gen_shipments.py
# Generates one shipment per non-cancelled order

import random
from datetime import date, timedelta
from helpers.constants import (
    COURIER_PARTNERS, TIER_1_CITIES,
)

random.seed(42)

TIER_1_CITY_NAMES = [c[0] for c in TIER_1_CITIES]


def generate_shipments(order_rows, warehouse_ids, customer_city_map):
    """
    Generate shipments for delivered/shipped orders.
    
    Args:
        order_rows: list of order tuples
        warehouse_ids: list of warehouse_id strings
        customer_city_map: dict {customer_id: city} for delivery time logic
    """

    shipments = []
    ship_counter = 0

    for order in order_rows:
        order_id = order[0]
        customer_id = order[1]
        order_date = order[2]
        order_status = order[3]

        # No shipment for cancelled or processing orders
        if order_status in ("Cancelled", "Processing"):
            continue

        ship_counter += 1
        shipment_id = f"SHIP{ship_counter:06d}"

        warehouse_id = random.choice(warehouse_ids)
        courier_partner = random.choice(COURIER_PARTNERS)

        # Shipped date: 1-3 days after order
        shipped_date = order_date + timedelta(days=random.randint(1, 3))

        # Promised delivery: 3-7 days after shipped
        customer_city = customer_city_map.get(customer_id, "Unknown")
        if customer_city in TIER_1_CITY_NAMES:
            promise_days = random.randint(2, 5)
        else:
            promise_days = random.randint(4, 8)

        promised_delivery_date = shipped_date + timedelta(days=promise_days)

        # Actual delivery date
        if order_status == "Delivered":
            # 70% on time, 20% late by 1-3 days, 10% late by 4-7 days
            delay_type = random.choices(
                ["on_time", "slight_delay", "major_delay"],
                weights=[0.70, 0.20, 0.10],
                k=1
            )[0]

            if delay_type == "on_time":
                actual_delivery_date = promised_delivery_date - timedelta(
                    days=random.randint(0, 1)
                )
            elif delay_type == "slight_delay":
                actual_delivery_date = promised_delivery_date + timedelta(
                    days=random.randint(1, 3)
                )
            else:
                actual_delivery_date = promised_delivery_date + timedelta(
                    days=random.randint(4, 7)
                )

            delivery_status = "Delivered"
        elif order_status == "Shipped":
            actual_delivery_date = None
            delivery_status = random.choice(["In Transit", "Out for Delivery"])
        else:
            actual_delivery_date = None
            delivery_status = "In Transit"

        shipments.append((
            shipment_id,
            order_id,
            warehouse_id,
            courier_partner,
            shipped_date,
            promised_delivery_date,
            actual_delivery_date,
            delivery_status,
        ))

    return shipments


SHIPMENTS_COLUMNS = [
    "shipment_id", "order_id", "warehouse_id", "courier_partner",
    "shipped_date", "promised_delivery_date", "actual_delivery_date",
    "delivery_status"
]