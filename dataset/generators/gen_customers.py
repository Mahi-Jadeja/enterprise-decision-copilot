# generators/gen_customers.py
# Generates ~1,000 realistic customer records

import random
from datetime import date, timedelta
from faker import Faker
from helpers.constants import (
    ALL_CITIES, TIER_1_CITIES, TIER_2_CITIES,
    GENDERS, GENDER_WEIGHTS,
    AGE_GROUPS, AGE_GROUP_WEIGHTS,
    LOYALTY_TIERS, LOYALTY_WEIGHTS,
    PAYMENT_MODES, PAYMENT_MODE_WEIGHTS,
)

fake = Faker("en_IN")
Faker.seed(42)
random.seed(42)

NUM_CUSTOMERS = 1000


def generate_customers():
    """Generate list of customer tuples ready for DB insertion."""

    customers = []

    # City distribution: 50% Tier-1, 30% Tier-2, 20% Tier-3
    city_pool = (
        TIER_1_CITIES * 6 +   # ~50%
        TIER_2_CITIES * 3 +   # ~30%
        [c for c in ALL_CITIES if c not in TIER_1_CITIES and c not in TIER_2_CITIES] * 2  # ~20%
    )

    for i in range(1, NUM_CUSTOMERS + 1):
        customer_id = f"CUST{i:05d}"

        # Signup date: spread over last 3 years
        days_ago = random.randint(1, 1095)
        signup_date = date.today() - timedelta(days=days_ago)

        city, state = random.choice(city_pool)

        gender = random.choices(GENDERS, weights=GENDER_WEIGHTS, k=1)[0]

        age_group = random.choices(AGE_GROUPS, weights=AGE_GROUP_WEIGHTS, k=1)[0]

        loyalty_tier = random.choices(LOYALTY_TIERS, weights=LOYALTY_WEIGHTS, k=1)[0]

        preferred_payment = random.choices(
            PAYMENT_MODES, weights=PAYMENT_MODE_WEIGHTS, k=1
        )[0]

        # Risk score: 1-100
        # Higher for COD preference, younger age groups
        base_risk = random.randint(10, 50)
        if preferred_payment == "COD":
            base_risk += random.randint(10, 30)
        if age_group == "18-24":
            base_risk += random.randint(5, 15)
        risk_score = min(base_risk, 100)

        # 90% active
        is_active = random.random() < 0.90

        customers.append((
            customer_id,
            signup_date,
            city,
            state,
            gender,
            age_group,
            loyalty_tier,
            preferred_payment,
            risk_score,
            is_active,
        ))

    return customers


CUSTOMERS_COLUMNS = [
    "customer_id", "signup_date", "city", "state", "gender",
    "age_group", "loyalty_tier", "preferred_payment_mode",
    "risk_score", "is_active"
]