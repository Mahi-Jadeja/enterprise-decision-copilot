# File 4: `docs/stage1_overview.md`

**Location:** `enterprise-decision-copilot/docs/stage1_overview.md`

```markdown
# Stage 1: Enterprise Dataset Design & Population

## Overview

Stage 1 is the **foundation** of the entire Enterprise Decision Copilot project. This stage focuses exclusively on building a realistic, enterprise-grade operational dataset that models a Myntra-like fashion e-commerce marketplace.

**No AI, no frontend, no backend logic** — just clean, well-structured data that can support everything that comes later.

---

## Stage 1 Goals

| Goal | Description | Success Criteria |
|------|-------------|------------------|
| **Realistic Data** | Data should feel like it came from a real business | Business logic is respected, distributions are realistic |
| **Complete Schema** | All core business processes are modeled | 13 tables covering full order lifecycle |
| **Query-Ready** | Data supports complex analytical queries | Sample queries run successfully |
| **Supabase Compatible** | Works within free tier limits | < 500MB, ~90k rows total |
| **Future-Proof** | Easy to build upon in later stages | Clean foreign keys, consistent IDs |

---

## Business Processes Modeled

### 1. Customer Management
- Customer registration and profiles
- Geographic distribution (cities, states)
- Segmentation (age groups, gender)
- Loyalty tiers (Bronze, Silver, Gold, Platinum)
- Risk scoring for fraud detection

### 2. Seller Onboarding
- Seller registration and verification
- Seller types (Individual, Business, Brand)
- Performance ratings (1.0 - 5.0)
- Commission rates (10% - 25%)
- Risk flagging (Low, Medium, High)

### 3. Product Catalog
- Fashion-specific categories
- Brand management
- Size and color variants
- Pricing (MRP vs Selling Price)
- Seasonal collections
- Return eligibility

### 4. Inventory & Warehouses
- Multi-warehouse inventory
- Stock levels (available, reserved, damaged)
- Real-time inventory tracking
- Geographic warehouse distribution

### 5. Orders & Checkout
- Multi-item orders
- Payment mode selection
- Discount application
- Order status tracking
- Channel attribution (App, Web, Mobile Web)

### 6. Payments
- Multiple payment methods
- Payment gateway tracking
- Payment status management
- COD vs Prepaid tracking

### 7. Shipping & Delivery
- Courier partner assignment
- Promised vs actual delivery dates
- Delivery status tracking
- Warehouse-based fulfillment

### 8. Returns & Refunds
- Return reason categorization
- Return type (Refund, Exchange)
- Pickup scheduling
- Refund processing
- Multiple refund methods

### 9. Seller Settlements
- Gross amount calculation
- Commission deduction
- Net payable computation
- Settlement status tracking

---

## Database Schema

### Entity-Relationship Summary

```
customers
    │
    ▼
orders ◄─────────────────────────────────────┐
    │                                        │
    ├──────► order_items ◄── products ◄── sellers
    │            │                │            │
    ├──────► payments            │            │
    │                            ▼            │
    └──────► shipments ◄── warehouses        │
                 │               │            │
                 │               ▼            │
                 │          inventory ────────┤
                 │               │            │
                 │               ▼            │
                 │    inventory_movements     │
                 │                            │
                 ▼                            │
            returns ──────► refunds           │
                 │                            │
                 └────► seller_settlements ◄──┘
```


### Table Relationships

| Parent Table | Child Table | Relationship |
|--------------|-------------|--------------|
| customers | orders | One customer has many orders |
| sellers | products | One seller has many products |
| sellers | inventory | One seller has many inventory records |
| sellers | order_items | One seller has many order items |
| sellers | seller_settlements | One seller has many settlements |
| products | inventory | One product has many inventory records |
| products | order_items | One product has many order items |
| warehouses | inventory | One warehouse has many inventory records |
| warehouses | shipments | One warehouse has many shipments |
| orders | order_items | One order has many items |
| orders | payments | One order has one payment |
| orders | shipments | One order has one shipment |
| order_items | returns | One order item has zero or one return |
| order_items | seller_settlements | One order item has one settlement |
| returns | refunds | One return has one refund |
| inventory | inventory_movements | One inventory has many movements |

---

## Data Volume and Distribution

### Row Counts

| Table | Target Rows | Rationale |
|-------|-------------|-----------|
| customers | 1,000 | Enough for variety, not too large |
| sellers | 150 | ~6-7 products per seller on average |
| products | 2,000 | Diverse catalog |
| warehouses | 10 | Realistic for India operations |
| inventory | 5,000 | ~2.5 warehouses per product average |
| inventory_movements | 25,000 | ~5 movements per inventory record |
| orders | 8,000 | ~8 orders per customer on average |
| order_items | 18,000 | ~2.25 items per order average |
| payments | 8,000 | 1:1 with orders |
| shipments | 8,000 | 1:1 with orders |
| returns | 2,500 | ~14% of order items returned |
| refunds | 2,500 | 1:1 with returns |
| seller_settlements | 12,000 | ~67% of order items settled |

**Total: ~92,000 rows** (within Supabase free tier)

### Key Distributions

#### Gender Split (Products)
- Men: 45%
- Women: 45%
- Kids: 10%

#### Payment Mode (Orders)
- Prepaid: 65%
- COD: 35%

#### Order Status Distribution
- Delivered: 70%
- Shipped: 10%
- Processing: 8%
- Cancelled: 7%
- Returned: 5%

#### Return Rate
- Overall: 25-30%
- Footwear: 35% (higher due to sizing)
- Women's Fashion: 30% (style preferences)
- Men's Basics: 15% (lower return rate)

#### Seller Performance (Pareto Principle)
- Top 20% sellers generate ~60% of GMV
- High-risk sellers have 40% higher return rates

#### Geographic Distribution
- Tier-1 Cities: 40% of customers
- Tier-2 Cities: 35% of customers
- Tier-3 Cities: 25% of customers

---

## Data Generation Rules

### Products

```python
# Category-Gender mapping
CATEGORIES = {
    'Men': ['Topwear', 'Bottomwear', 'Footwear', 'Accessories'],
    'Women': ['Topwear', 'Bottomwear', 'Dresses', 'Footwear', 'Accessories'],
    'Kids': ['Topwear', 'Bottomwear', 'Footwear']
}

# Size rules
SIZES = {
    'Footwear': ['6', '7', '8', '9', '10', '11'],
    'Accessories': ['Free Size'],
    'default': ['XS', 'S', 'M', 'L', 'XL', 'XXL']
}

# Pricing rule
selling_price = mrp * random.uniform(0.5, 0.95)

### Orders

```python
# Items per order: weighted distribution
items_per_order = random.choices([1, 2, 3], weights=[50, 35, 15])[0]

# Order date: last 12 months with seasonal peaks
# Higher orders during: Oct-Nov (Diwali), Dec-Jan (Winter Sale)

# Payment mode based on customer risk
if customer_risk_score > 7:
    payment_mode = 'COD'  # Higher risk customers prefer COD
else:
    payment_mode = random.choices(['Prepaid', 'COD'], weights=[65, 35])[0]
```

### Returns

```python
# Return probability factors
base_return_rate = 0.25

# Category modifier
if category == 'Footwear':
    return_rate *= 1.4
elif category == 'Dresses':
    return_rate *= 1.2

# Seller risk modifier
if seller_risk == 'High':
    return_rate *= 1.3

# Delivery delay modifier
if delivery_delayed:
    return_rate *= 1.25
```

### Shipments

```python
# Delivery time based on city tier
DELIVERY_DAYS = {
    'Tier-1': (2, 4),   # 2-4 days
    'Tier-2': (3, 6),   # 3-6 days
    'Tier-3': (5, 10)   # 5-10 days
}

# Delay probability
delay_probability = 0.15  # 15% orders delayed
```

---

## Data Integrity Rules

### Foreign Key Constraints

All foreign keys are enforced:

```sql
-- Example: order_items references orders, products, sellers
order_id VARCHAR REFERENCES orders(order_id)
product_id VARCHAR REFERENCES products(product_id)
seller_id VARCHAR REFERENCES sellers(seller_id)
```

### Insert Order (Critical!)

Tables must be populated in this exact order:

1. `customers` (no dependencies)
2. `sellers` (no dependencies)
3. `warehouses` (no dependencies)
4. `products` (depends on sellers)
5. `inventory` (depends on products, sellers, warehouses)
6. `orders` (depends on customers)
7. `order_items` (depends on orders, products, sellers)
8. `payments` (depends on orders)
9. `shipments` (depends on orders, warehouses)
10. `inventory_movements` (depends on inventory)
11. `returns` (depends on order_items)
12. `refunds` (depends on returns)
13. `seller_settlements` (depends on sellers, order_items)

### Referential Integrity Checks

```sql
-- Verify no orphan records
SELECT COUNT(*) FROM order_items oi 
LEFT JOIN orders o ON oi.order_id = o.order_id 
WHERE o.order_id IS NULL;
-- Should return 0

-- Verify all returns have valid order_items
SELECT COUNT(*) FROM returns r 
LEFT JOIN order_items oi ON r.order_item_id = oi.order_item_id 
WHERE oi.order_item_id IS NULL;
-- Should return 0
```

---

## Stage 1 Completion Checklist

- [ ] Schema created in Supabase without errors
- [ ] All 13 tables exist with correct columns
- [ ] Foreign key relationships are correct
- [ ] Python population script runs without errors
- [ ] Row counts match targets (within 10% variance)
- [ ] Sample queries execute successfully
- [ ] Data distributions are realistic
- [ ] No orphan records exist
- [ ] Documentation is complete

---

## What Comes Next (Stage 2)

After Stage 1 is frozen, we move to:

**Stage 2: Data Access Layer**
- FastAPI backend service
- Safe SQL query execution
- API endpoints for data retrieval
- Query validation and sanitization
- Preparation for AI integration

---

## Notes and Assumptions

### Assumptions Made

1. **Single Currency**: All amounts in INR
2. **Single Country**: India only (states, cities)
3. **No User Auth**: Dataset only, no login system
4. **Simplified Logistics**: One shipment per order
5. **No Exchanges Yet**: Returns are refund-only for simplicity
6. **Point-in-Time Data**: Represents ~12 months of operations

### Known Simplifications

1. **No Product Variants Table**: Sizes/colors are attributes, not separate SKUs
2. **No Promotions Table**: Discounts are order-level only
3. **No Reviews Table**: Ratings are at seller level only
4. **No Cart/Wishlist**: Only completed orders

These can be added in future iterations if needed.

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Foreign key violation | Wrong insert order | Follow exact insert order above |
| Connection timeout | Supabase cold start | Retry after 30 seconds |
| Duplicate key error | Script re-run | Truncate tables or use UPSERT |
| SSL error | Missing SSL mode | Add `?sslmode=require` to connection string |

### Reset Database

```sql
-- WARNING: This drops all data!
TRUNCATE TABLE seller_settlements, refunds, returns, 
               inventory_movements, shipments, payments, 
               order_items, orders, inventory, products, 
               warehouses, sellers, customers CASCADE;
```

---

