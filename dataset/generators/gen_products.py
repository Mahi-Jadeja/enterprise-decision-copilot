# generators/gen_products.py
# Generates ~2,000 realistic product records

import random
from helpers.constants import (
    BRANDS, CATEGORY_MAP, CATEGORY_WEIGHTS,
    CLOTHING_SIZES, FOOTWEAR_SIZES,
    COLORS, SEASONS, SEASON_WEIGHTS,
    MRP_RANGES,
)

random.seed(42)

NUM_PRODUCTS = 2000


def generate_products(seller_ids):
    """
    Generate product tuples.
    
    Args:
        seller_ids: list of valid seller_id strings
    
    Business rules:
        - Top 20% sellers get ~60% of products
        - Gender distribution affects category selection
        - Size depends on category
        - selling_price < MRP
    """

    products = []

    # Top 20% sellers get more products (Pareto distribution)
    num_top_sellers = max(1, int(len(seller_ids) * 0.20))
    top_sellers = seller_ids[:num_top_sellers]
    other_sellers = seller_ids[num_top_sellers:]

    # Build weighted seller pool: top sellers appear ~3x more
    seller_pool = top_sellers * 4 + other_sellers

    for i in range(1, NUM_PRODUCTS + 1):
        product_id = f"PROD{i:05d}"

        seller_id = random.choice(seller_pool)

        brand = random.choice(BRANDS)

        # Determine product gender context
        product_gender = random.choices(
            ["Male", "Female", "Unisex"],
            weights=[0.45, 0.45, 0.10],
            k=1
        )[0]

        # Pick category based on gender weights
        cat_weights = CATEGORY_WEIGHTS[product_gender]
        categories = list(cat_weights.keys())
        weights = list(cat_weights.values())

        # If weights sum to 0 for a category (e.g., Male + Dresses), 
        # filter them out
        valid = [(c, w) for c, w in zip(categories, weights) if w > 0]
        if not valid:
            valid = [("Topwear", 1.0)]
        
        cats, wts = zip(*valid)
        category = random.choices(cats, weights=wts, k=1)[0]

        sub_category = random.choice(CATEGORY_MAP[category])

        # Size depends on category
        if category == "Footwear":
            size = random.choice(FOOTWEAR_SIZES)
        elif category == "Accessories":
            size = "Free Size"
        else:
            size = random.choice(CLOTHING_SIZES)

        color = random.choice(COLORS)

        # MRP based on category
        mrp_low, mrp_high = MRP_RANGES[category]
        mrp = round(random.uniform(mrp_low, mrp_high), 2)

        # Selling price: 60-95% of MRP
        discount_pct = random.uniform(0.05, 0.40)
        selling_price = round(mrp * (1 - discount_pct), 2)

        season = random.choices(SEASONS, weights=SEASON_WEIGHTS, k=1)[0]

        # Accessories are non-returnable 30% of the time
        if category == "Accessories":
            is_returnable = random.random() > 0.30
        else:
            is_returnable = True

        products.append((
            product_id,
            seller_id,
            brand,
            category,
            sub_category,
            size,
            color,
            mrp,
            selling_price,
            season,
            is_returnable,
        ))

    return products


PRODUCTS_COLUMNS = [
    "product_id", "seller_id", "brand", "category", "sub_category",
    "size", "color", "mrp", "selling_price", "season", "is_returnable"
]