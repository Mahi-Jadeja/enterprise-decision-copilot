# helpers/constants.py
# Shared constants, lists, and business rules used across all generators

import random

# ============================================================
# GEOGRAPHIC DATA
# ============================================================

TIER_1_CITIES = [
    ("Mumbai", "Maharashtra"),
    ("Delhi", "Delhi"),
    ("Bangalore", "Karnataka"),
    ("Hyderabad", "Telangana"),
    ("Chennai", "Tamil Nadu"),
    ("Kolkata", "West Bengal"),
    ("Pune", "Maharashtra"),
    ("Ahmedabad", "Gujarat"),
]

TIER_2_CITIES = [
    ("Jaipur", "Rajasthan"),
    ("Lucknow", "Uttar Pradesh"),
    ("Chandigarh", "Punjab"),
    ("Indore", "Madhya Pradesh"),
    ("Nagpur", "Maharashtra"),
    ("Bhopal", "Madhya Pradesh"),
    ("Coimbatore", "Tamil Nadu"),
    ("Kochi", "Kerala"),
    ("Visakhapatnam", "Andhra Pradesh"),
    ("Vadodara", "Gujarat"),
]

TIER_3_CITIES = [
    ("Ranchi", "Jharkhand"),
    ("Raipur", "Chhattisgarh"),
    ("Mysuru", "Karnataka"),
    ("Jodhpur", "Rajasthan"),
    ("Guwahati", "Assam"),
    ("Dehradun", "Uttarakhand"),
    ("Jammu", "Jammu and Kashmir"),
    ("Agra", "Uttar Pradesh"),
    ("Varanasi", "Uttar Pradesh"),
    ("Meerut", "Uttar Pradesh"),
]

ALL_CITIES = TIER_1_CITIES + TIER_2_CITIES + TIER_3_CITIES

# ============================================================
# CUSTOMER CONSTANTS
# ============================================================

GENDERS = ["Male", "Female", "Non-Binary"]
GENDER_WEIGHTS = [0.45, 0.45, 0.10]

AGE_GROUPS = ["18-24", "25-34", "35-44", "45-54", "55+"]
AGE_GROUP_WEIGHTS = [0.25, 0.35, 0.20, 0.12, 0.08]

LOYALTY_TIERS = ["Bronze", "Silver", "Gold", "Platinum"]
LOYALTY_WEIGHTS = [0.40, 0.30, 0.20, 0.10]

PAYMENT_MODES = ["UPI", "Credit Card", "Debit Card", "Net Banking", "COD", "Wallet"]
PAYMENT_MODE_WEIGHTS = [0.25, 0.20, 0.15, 0.10, 0.20, 0.10]

# ============================================================
# SELLER CONSTANTS
# ============================================================

SELLER_TYPES = ["Individual", "Brand Official", "Authorized Reseller"]
SELLER_TYPE_WEIGHTS = [0.50, 0.20, 0.30]

SELLER_REGIONS = ["North", "South", "East", "West", "Central", "Pan-India"]
SELLER_REGION_WEIGHTS = [0.20, 0.25, 0.10, 0.20, 0.10, 0.15]

RISK_FLAGS = ["Low", "Medium", "High"]
RISK_FLAG_WEIGHTS = [0.60, 0.25, 0.15]

# ============================================================
# PRODUCT CONSTANTS
# ============================================================

BRANDS = [
    "Roadster", "HRX", "Mast & Harbour", "HERE&NOW", "DressBerry",
    "Anouk", "Libas", "W", "Biba", "FabIndia",
    "Nike", "Adidas", "Puma", "Reebok", "Skechers",
    "Levi's", "Wrangler", "Allen Solly", "Van Heusen", "Peter England",
    "H&M", "Zara", "ONLY", "Vero Moda", "Jack & Jones",
    "Wildcraft", "Fastrack", "Fossil", "Titan", "Lavie"
]

# Category -> Sub-categories mapping
CATEGORY_MAP = {
    "Topwear": ["T-Shirts", "Shirts", "Kurtas", "Tops", "Sweatshirts"],
    "Bottomwear": ["Jeans", "Trousers", "Shorts", "Palazzos", "Leggings"],
    "Footwear": ["Sneakers", "Sandals", "Formal Shoes", "Sports Shoes", "Flip-Flops"],
    "Dresses": ["Maxi Dress", "A-Line Dress", "Bodycon Dress", "Shirt Dress", "Wrap Dress"],
    "Accessories": ["Bags", "Watches", "Sunglasses", "Belts", "Wallets"],
}

CATEGORY_WEIGHTS = {
    "Male":   {"Topwear": 0.30, "Bottomwear": 0.25, "Footwear": 0.25, "Dresses": 0.00, "Accessories": 0.20},
    "Female": {"Topwear": 0.20, "Bottomwear": 0.15, "Footwear": 0.20, "Dresses": 0.25, "Accessories": 0.20},
    "Unisex": {"Topwear": 0.25, "Bottomwear": 0.20, "Footwear": 0.25, "Dresses": 0.05, "Accessories": 0.25},
}

CLOTHING_SIZES = ["XS", "S", "M", "L", "XL", "XXL"]
FOOTWEAR_SIZES = ["6", "7", "8", "9", "10", "11"]

COLORS = [
    "Black", "White", "Navy Blue", "Grey", "Red",
    "Blue", "Green", "Maroon", "Pink", "Beige",
    "Brown", "Yellow", "Orange", "Olive", "Teal"
]

SEASONS = ["Spring", "Summer", "Monsoon", "Winter", "All-Season"]
SEASON_WEIGHTS = [0.15, 0.25, 0.15, 0.20, 0.25]

# MRP ranges by category
MRP_RANGES = {
    "Topwear": (399, 2999),
    "Bottomwear": (499, 3499),
    "Footwear": (599, 5999),
    "Dresses": (699, 4999),
    "Accessories": (299, 7999),
}

# ============================================================
# WAREHOUSE CONSTANTS
# ============================================================

WAREHOUSE_LOCATIONS = [
    ("Mumbai", "Maharashtra", "Fulfillment Center"),
    ("Delhi", "Delhi", "Fulfillment Center"),
    ("Bangalore", "Karnataka", "Fulfillment Center"),
    ("Hyderabad", "Telangana", "Fulfillment Center"),
    ("Chennai", "Tamil Nadu", "Fulfillment Center"),
    ("Kolkata", "West Bengal", "Distribution Hub"),
    ("Pune", "Maharashtra", "Distribution Hub"),
    ("Jaipur", "Rajasthan", "Distribution Hub"),
    ("Lucknow", "Uttar Pradesh", "Distribution Hub"),
    ("Kochi", "Kerala", "Distribution Hub"),
]

# ============================================================
# ORDER CONSTANTS
# ============================================================

ORDER_STATUSES = ["Delivered", "Shipped", "Processing", "Cancelled"]
ORDER_STATUS_WEIGHTS = [0.65, 0.10, 0.05, 0.20]

ORDER_CHANNELS = ["App", "Website", "Mobile Web"]
ORDER_CHANNEL_WEIGHTS = [0.55, 0.30, 0.15]

ORDER_PAYMENT_MODES = ["COD", "Prepaid"]
ORDER_PAYMENT_WEIGHTS = [0.35, 0.65]

ITEM_STATUSES_DELIVERED = ["Delivered", "Returned"]
ITEM_STATUSES_OTHER = ["Shipped", "Processing", "Cancelled"]

# ============================================================
# SHIPMENT CONSTANTS
# ============================================================

COURIER_PARTNERS = ["Delhivery", "BlueDart", "Ecom Express", "DTDC", "Shadowfax"]
DELIVERY_STATUSES = ["Delivered", "In Transit", "Out for Delivery", "RTO", "Lost"]

# ============================================================
# RETURN CONSTANTS
# ============================================================

RETURN_REASONS = [
    "Size Mismatch", "Color Different from Image", "Defective Product",
    "Wrong Item Delivered", "Quality Not as Expected", "Changed Mind",
    "Better Price Available", "Late Delivery"
]

RETURN_TYPES = ["Return", "Exchange"]
RETURN_TYPE_WEIGHTS = [0.70, 0.30]

RETURN_STATUSES = ["Initiated", "Picked Up", "Received", "Completed", "Rejected"]

# ============================================================
# PAYMENT CONSTANTS
# ============================================================

PAYMENT_METHODS_PREPAID = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Wallet"]
PAYMENT_GATEWAYS = ["Razorpay", "Paytm", "PhonePe", "Stripe", "PayU"]

# ============================================================
# SETTLEMENT CONSTANTS
# ============================================================

SETTLEMENT_STATUSES = ["Pending", "Processed", "Paid", "On Hold"]
SETTLEMENT_STATUS_WEIGHTS = [0.15, 0.25, 0.50, 0.10]

# ============================================================
# RETURN RATE CONFIG (by category — higher for footwear/dresses)
# ============================================================

RETURN_RATE_BY_CATEGORY = {
    "Topwear": 0.20,
    "Bottomwear": 0.22,
    "Footwear": 0.35,
    "Dresses": 0.30,
    "Accessories": 0.10,
}