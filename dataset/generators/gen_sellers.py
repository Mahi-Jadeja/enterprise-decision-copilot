# generators/gen_sellers.py
# Generates ~150 realistic seller records

import random
from datetime import date, timedelta
from faker import Faker
from helpers.constants import (
    SELLER_TYPES, SELLER_TYPE_WEIGHTS,
    SELLER_REGIONS, SELLER_REGION_WEIGHTS,
    RISK_FLAGS, RISK_FLAG_WEIGHTS,
)

fake = Faker("en_IN")
Faker.seed(42)
random.seed(42)

NUM_SELLERS = 150

# Realistic Indian fashion seller names
SELLER_NAME_PREFIXES = [
    "Fashion", "Style", "Trendy", "Urban", "Classic",
    "Royal", "Desi", "Modern", "Elite", "Prime",
    "Star", "Golden", "Diamond", "Silver", "Mega",
]

SELLER_NAME_SUFFIXES = [
    "Traders", "Fashions", "Apparels", "Collections", "Hub",
    "Store", "Bazaar", "Mart", "Boutique", "Gallery",
    "Styles", "Creations", "Wears", "Threads", "Trends",
]


def _generate_seller_name(index):
    """Generate a unique seller business name."""
    prefix = SELLER_NAME_PREFIXES[index % len(SELLER_NAME_PREFIXES)]
    suffix = SELLER_NAME_SUFFIXES[index % len(SELLER_NAME_SUFFIXES)]
    # Add a number for uniqueness
    return f"{prefix} {suffix} {index}"


def generate_sellers():
    """Generate list of seller tuples ready for DB insertion."""

    sellers = []

    for i in range(1, NUM_SELLERS + 1):
        seller_id = f"SELL{i:04d}"

        seller_name = _generate_seller_name(i)

        seller_type = random.choices(
            SELLER_TYPES, weights=SELLER_TYPE_WEIGHTS, k=1
        )[0]

        # Onboarding date: spread over last 4 years
        days_ago = random.randint(30, 1460)
        onboarding_date = date.today() - timedelta(days=days_ago)

        # Seller rating: 2.5 to 5.0
        # Brand Official sellers tend to have higher ratings
        if seller_type == "Brand Official":
            seller_rating = round(random.uniform(3.5, 5.0), 1)
        elif seller_type == "Authorized Reseller":
            seller_rating = round(random.uniform(3.0, 4.8), 1)
        else:
            seller_rating = round(random.uniform(2.5, 4.5), 1)

        seller_region = random.choices(
            SELLER_REGIONS, weights=SELLER_REGION_WEIGHTS, k=1
        )[0]

        # Commission rate: 5% to 25%
        # Brand Official pays less commission (they have leverage)
        if seller_type == "Brand Official":
            commission_rate = round(random.uniform(5.0, 12.0), 2)
        else:
            commission_rate = round(random.uniform(10.0, 25.0), 2)

        risk_flag = random.choices(
            RISK_FLAGS, weights=RISK_FLAG_WEIGHTS, k=1
        )[0]

        # Low-rated sellers more likely to be high risk
        if seller_rating < 3.0:
            risk_flag = random.choices(
                ["Medium", "High"], weights=[0.4, 0.6], k=1
            )[0]

        # 92% active
        is_active = random.random() < 0.92

        sellers.append((
            seller_id,
            seller_name,
            seller_type,
            onboarding_date,
            seller_rating,
            seller_region,
            commission_rate,
            risk_flag,
            is_active,
        ))

    return sellers


SELLERS_COLUMNS = [
    "seller_id", "seller_name", "seller_type", "onboarding_date",
    "seller_rating", "seller_region", "commission_rate",
    "risk_flag", "is_active"
]