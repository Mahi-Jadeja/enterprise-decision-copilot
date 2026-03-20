# 📐 Data Rules & Business Logic

## Enterprise Decision Copilot — Stage 1

This document describes every business rule, assumption, distribution,
and constraint applied during synthetic data generation.

Any future contributor, mentor, or reviewer should read this file
to understand **why** the data looks the way it does.

---

## Table of Contents

1. [Global Conventions](#1-global-conventions)
2. [Customers](#2-customers)
3. [Sellers](#3-sellers)
4. [Products](#4-products)
5. [Warehouses](#5-warehouses)
6. [Inventory](#6-inventory)
7. [Inventory Movements](#7-inventory-movements)
8. [Orders](#8-orders)
9. [Order Items](#9-order-items)
10. [Payments](#10-payments)
11. [Shipments](#11-shipments)
12. [Returns](#12-returns)
13. [Refunds](#13-refunds)
14. [Seller Settlements](#14-seller-settlements)
15. [Cross-Table Integrity Rules](#15-cross-table-integrity-rules)
16. [Known Simplifications](#16-known-simplifications)

---

## 1. Global Conventions

| Convention | Detail |
|---|---|
| **ID Format** | Human-readable VARCHAR (e.g., `CUST00001`, `ORD000001`) |
| **Currency** | Indian Rupees (INR), stored as `NUMERIC(10,2)` |
| **Dates** | PostgreSQL `DATE` or `TIMESTAMP`, no timezone |
| **Booleans** | PostgreSQL native `BOOLEAN` |
| **Random Seed** | `42` for all generators — ensures reproducibility |
| **Locale** | `en_IN` (Indian English) for Faker-generated values |
| **NULL Policy** | NULLs used only where business logic requires (e.g., `actual_delivery_date` for in-transit shipments) |

---

## 2. Customers

**Table:** `customers`
**Target Rows:** ~1,000

### Distributions

| Field | Rule |
|---|---|
| `customer_id` | `CUST00001` to `CUST01000` |
| `signup_date` | Random date within last **3 years** from today |
| `city`, `state` | Drawn from curated Indian city list |
| City tier split | **50% Tier-1**, **30% Tier-2**, **20% Tier-3** |
| `gender` | **45% Male**, **45% Female**, **10% Non-Binary** |
| `age_group` | 18-24 (25%), 25-34 (35%), 35-44 (20%), 45-54 (12%), 55+ (8%) |
| `loyalty_tier` | Bronze (40%), Silver (30%), Gold (20%), Platinum (10%) |
| `preferred_payment_mode` | UPI (25%), Credit Card (20%), COD (20%), Debit Card (15%), Wallet (10%), Net Banking (10%) |
| `risk_score` | Base 10-50, +10-30 for COD preference, +5-15 for age 18-24, capped at 100 |
| `is_active` | **90% TRUE**, 10% FALSE |

### Business Rationale

- Tier-1 city dominance mirrors real Myntra user base
- Young users and COD users are legitimately higher risk (more returns, fraud attempts)
- Loyalty tiers follow a realistic pyramid shape
- 10% inactive accounts simulate churn

### Tier Classification

| Tier | Cities |
|---|---|
| **Tier-1** | Mumbai, Delhi, Bangalore, Hyderabad, Chennai, Kolkata, Pune, Ahmedabad |
| **Tier-2** | Jaipur, Lucknow, Chandigarh, Indore, Nagpur, Bhopal, Coimbatore, Kochi, Visakhapatnam, Vadodara |
| **Tier-3** | Ranchi, Raipur, Mysuru, Jodhpur, Guwahati, Dehradun, Jammu, Agra, Varanasi, Meerut |

---

## 3. Sellers

**Table:** `sellers`
**Target Rows:** ~150

### Distributions

| Field | Rule |
|---|---|
| `seller_id` | `SELL0001` to `SELL0150` |
| `seller_name` | Generated from prefix + suffix combinations (e.g., "Fashion Traders 12") |
| `seller_type` | Individual (50%), Authorized Reseller (30%), Brand Official (20%) |
| `onboarding_date` | Random date within last **4 years** |
| `seller_rating` | Brand Official: 3.5-5.0, Authorized Reseller: 3.0-4.8, Individual: 2.5-4.5 |
| `seller_region` | South (25%), North (20%), West (20%), Pan-India (15%), Central (10%), East (10%) |
| `commission_rate` | Brand Official: 5-12%, Others: 10-25% |
| `risk_flag` | Low (60%), Medium (25%), High (15%) |
| `is_active` | **92% TRUE** |

### Business Rules

- **Sellers rated below 3.0** are forced to Medium or High risk (60% High, 40% Medium)
- **Brand Official sellers** pay lower commission (they bring brand value)
- **Top 20% of sellers** receive ~60% of product listings (Pareto principle)
- **High-risk sellers** generate higher return rates (1.5x multiplier)

---

## 4. Products

**Table:** `products`
**Target Rows:** ~2,000

### Distributions

| Field | Rule |
|---|---|
| `product_id` | `PROD00001` to `PROD02000` |
| `seller_id` | Top 20% sellers get ~60% of products |
| `brand` | 30 realistic Indian & international fashion brands |
| Product gender context | **45% Male**, **45% Female**, **10% Unisex** |
| `category` | Weighted by gender (see table below) |
| `sub_category` | 5 sub-categories per category |
| `size` | Clothing: XS-XXL, Footwear: 6-11, Accessories: "Free Size" |
| `color` | 15 common fashion colors |
| `mrp` | Category-dependent ranges (see table below) |
| `selling_price` | **60-95% of MRP** (discount 5-40%) |
| `season` | Spring (15%), Summer (25%), Monsoon (15%), Winter (20%), All-Season (25%) |
| `is_returnable` | TRUE for all except 30% of Accessories |

### Category Weights by Gender

| Category | Male | Female | Unisex |
|---|---|---|---|
| Topwear | 30% | 20% | 25% |
| Bottomwear | 25% | 15% | 20% |
| Footwear | 25% | 20% | 25% |
| Dresses | 0% | 25% | 5% |
| Accessories | 20% | 20% | 25% |

### MRP Ranges by Category

| Category | Min MRP (₹) | Max MRP (₹) |
|---|---|---|
| Topwear | 399 | 2,999 |
| Bottomwear | 499 | 3,499 |
| Footwear | 599 | 5,999 |
| Dresses | 699 | 4,999 |
| Accessories | 299 | 7,999 |

### Business Rationale

- Selling price is **always** less than MRP (legal requirement in India)
- Dresses are only for Female/Unisex (no male dresses in Myntra context)
- Accessories have wider price range (belts vs luxury watches)
- Non-returnable accessories simulate "final sale" items

---

## 5. Warehouses

**Table:** `warehouses`
**Target Rows:** 10 (fixed)

### Locations

| ID | City | State | Type |
|---|---|---|---|
| WH001 | Mumbai | Maharashtra | Fulfillment Center |
| WH002 | Delhi | Delhi | Fulfillment Center |
| WH003 | Bangalore | Karnataka | Fulfillment Center |
| WH004 | Hyderabad | Telangana | Fulfillment Center |
| WH005 | Chennai | Tamil Nadu | Fulfillment Center |
| WH006 | Kolkata | West Bengal | Distribution Hub |
| WH007 | Pune | Maharashtra | Distribution Hub |
| WH008 | Jaipur | Rajasthan | Distribution Hub |
| WH009 | Lucknow | Uttar Pradesh | Distribution Hub |
| WH010 | Kochi | Kerala | Distribution Hub |

### Business Rationale

- 5 Fulfillment Centers in major metros (handle full order processing)
- 5 Distribution Hubs in Tier-1/2 cities (last-mile distribution)
- All warehouses start as active
- This mirrors how Myntra/Flipkart structure their logistics

---

## 6. Inventory

**Table:** `inventory`
**Target Rows:** ~5,000

### Rules

| Field | Rule |
|---|---|
| `inventory_id` | `INV000001` to `INV00XXXX` |
| Products per warehouse | Each product stocked in **1-4 warehouses** (weighted: 1→20%, 2→35%, 3→30%, 4→15%) |
| `seller_id` | Inherited from the product's seller |
| `available_qty` | Gaussian distribution, mean=40, std=25, min=0 |
| `reserved_qty` | 0 to 10% of available quantity |
| `damaged_qty` | 0 to 3% of available quantity |
| `last_updated` | Within last 30 days |

### Business Rationale

- Not every product is in every warehouse (realistic partial distribution)
- Reserved quantity represents items in carts / being processed
- Damaged quantity represents QC failures, customer returns with damage
- One product can have multiple inventory records (one per warehouse)

---

## 7. Inventory Movements

**Table:** `inventory_movements`
**Target Rows:** ~25,000

### Movement Types

| Type | Source | Quantity | Reference |
|---|---|---|---|
| `INBOUND` | Initial stock load | available_qty + 5-50 buffer | `INITIAL_STOCK` |
| `OUTBOUND` | Order fulfillment | order item quantity | `order_item_id` |
| `RETURN_INBOUND` | Customer returns | 1 per return | `return_id` |
| `ADJUSTMENT` | Damage/loss audits | -1 to -5 | `DAMAGE_AUDIT` |

### Rules

- Every inventory record gets exactly **1 INBOUND** movement
- Every order item generates exactly **1 OUTBOUND** movement
- Only **Received/Completed** returns generate RETURN_INBOUND
- **~500 random ADJUSTMENT** movements simulate warehouse audits
- Movement dates spread across realistic time windows

---

## 8. Orders

**Table:** `orders`
**Target Rows:** ~8,000

### Distributions

| Field | Rule |
|---|---|
| `order_id` | `ORD000001` to `ORD008000` |
| `customer_id` | Random selection from all customers |
| `order_date` | Random date within last **18 months** |
| `order_status` | Delivered (65%), Cancelled (20%), Shipped (10%), Processing (5%) |
| `payment_mode` | **COD (35%)**, **Prepaid (65%)** |
| `order_channel` | App (55%), Website (30%), Mobile Web (15%) |
| Items per order | **1 item (50%)**, **2 items (35%)**, **3 items (15%)** |
| `discount_amount` | 0-30% of total, weighted toward lower discounts |
| `final_payable` | `total_amount - discount_amount` |

### Discount Distribution

| Discount % | Probability |
|---|---|
| 0% (no discount) | 25% |
| 5% | 15% |
| 10% | 20% |
| 15% | 15% |
| 20% | 10% |
| 25% | 10% |
| 30% | 5% |

### Business Rationale

- 65% delivery rate is realistic for Indian e-commerce
- 20% cancellation rate reflects COD non-acceptance + customer changes
- COD at 35% matches real Indian market behavior
- App-dominant channel reflects mobile-first market
- No duplicate products in a single order

---

## 9. Order Items

**Table:** `order_items`
**Target Rows:** ~18,000

### Rules

| Field | Rule |
|---|---|
| `order_item_id` | `OI0000001` to `OI00XXXXX` |
| `order_id` | Parent order reference |
| `product_id` | Randomly selected, no duplicates within same order |
| `seller_id` | Inherited from the product |
| `quantity` | **1 unit (85%)**, **2 units (15%)** |
| `item_price` | `selling_price × quantity` |
| `item_status` | Mirrors parent order status |

### Item Status Mapping

| Order Status | Item Status |
|---|---|
| Delivered | Delivered |
| Cancelled | Cancelled |
| Shipped | Shipped |
| Processing | Processing |

---

## 10. Payments

**Table:** `payments`
**Target Rows:** ~8,000 (1 per order)

### Rules

| Field | Rule |
|---|---|
| `payment_id` | `PAY000001` to `PAY008000` |
| `payment_method` | If COD → "COD", if Prepaid → one of UPI/Credit Card/Debit Card/Net Banking/Wallet |
| `payment_status` | Cancelled orders → "Failed", COD+not-delivered → "Pending", else → "Completed" |
| `payment_date` | Order date + 0-12 hours |
| `paid_amount` | Failed → ₹0, else → `final_payable` |
| `gateway` | COD → "COD", Prepaid → one of Razorpay/Paytm/PhonePe/Stripe/PayU |

### Payment Status Logic
IF order is Cancelled → Failed
IF COD + not yet delivered → Pending
ELSE → Completed


---

## 11. Shipments

**Table:** `shipments`
**Target Rows:** ~6,000 (only non-cancelled, non-processing orders)

### Rules

| Field | Rule |
|---|---|
| `shipment_id` | `SHIP000001` to `SHIP00XXXX` |
| `order_id` | Only orders with status Delivered or Shipped |
| `warehouse_id` | Random warehouse |
| `courier_partner` | Delhivery, BlueDart, Ecom Express, DTDC, Shadowfax |
| `shipped_date` | Order date + 1-3 days |
| `promised_delivery_date` | Shipped date + 2-5 days (Tier-1) or 4-8 days (others) |
| `actual_delivery_date` | See delay rules below. NULL if not delivered. |
| `delivery_status` | Delivered / In Transit / Out for Delivery / RTO / Lost |

### Delivery Delay Distribution (Delivered Orders Only)

| Scenario | Probability | Actual vs Promised |
|---|---|---|
| On time | 70% | 0-1 days early |
| Slight delay | 20% | 1-3 days late |
| Major delay | 10% | 4-7 days late |

### Shipment Exclusions

- **Cancelled** orders → NO shipment created
- **Processing** orders → NO shipment created

### Business Rationale

- Tier-1 cities get faster promised delivery (closer to fulfillment centers)
- Delivery delays correlate with higher return probability
- ~30% of shipments experience some delay (realistic for India)

---

## 12. Returns

**Table:** `returns`
**Target Rows:** ~2,500

### Return Rate by Category

| Category | Base Return Rate |
|---|---|
| Accessories | 10% |
| Topwear | 20% |
| Bottomwear | 22% |
| Dresses | 30% |
| Footwear | **35%** |

### Risk Multipliers

| Seller Risk Flag | Multiplier |
|---|---|
| Low | 1.0x (no change) |
| Medium | 1.2x |
| High | **1.5x** |

### Rules

| Field | Rule |
|---|---|
| `return_id` | `RET000001` to `RET00XXXX` |
| `order_item_id` | Only **Delivered** items with `is_returnable = TRUE` |
| `return_date` | Delivery date + 2-15 days |
| `return_reason` | One of 8 realistic reasons |
| `return_type` | Return (70%), Exchange (30%) |
| `return_status` | Completed (65%), Received (10%), Picked Up (10%), Initiated (5%), Rejected (10%) |
| `pickup_date` | Return date + 1-5 days (only if Picked Up/Received/Completed) |
| `refund_amount` | Exchange → ₹0, Return → 80% full refund, 20% partial (90-100%) |

### Return Reasons

1. Size Mismatch
2. Color Different from Image
3. Defective Product
4. Wrong Item Delivered
5. Quality Not as Expected
6. Changed Mind
7. Better Price Available
8. Late Delivery

### Business Rationale

- Footwear has highest returns (sizing is hardest to get right online)
- High-risk sellers naturally generate more returns (poor quality/service)
- Non-returnable items (some accessories) are excluded
- Exchange returns don't trigger refund amount
- Overall return rate targets ~25-30% of delivered items

---

## 13. Refunds

**Table:** `refunds`
**Target Rows:** ~1,500-2,000

### Rules

| Field | Rule |
|---|---|
| `refund_id` | `REF000001` to `REF00XXXX` |
| `return_id` | Only returns with status **Completed** AND `refund_amount > 0` |
| `refund_method` | Original Payment Method (50%), Myntra Credit (30%), Bank Transfer (20%) |
| `refund_status` | Completed (90%), Processing (7%), Failed (3%) |
| `refund_date` | Return date + 2-7 days |
| `refunded_amount` | Failed → ₹0, else → matches return's `refund_amount` |

### Refund Exclusions

- Returns with status other than **Completed** → NO refund
- Exchange returns (`refund_amount = 0`) → NO refund
- Rejected returns → NO refund

---

## 14. Seller Settlements

**Table:** `seller_settlements`
**Target Rows:** ~12,000

### Rules

| Field | Rule |
|---|---|
| `settlement_id` | `SETT000001` to `SETT0XXXXX` |
| `seller_id` | From the order item's seller |
| `order_item_id` | Only **Delivered** items |
| `gross_amount` | = `item_price` |
| `commission_amount` | = `gross_amount × seller's commission_rate` |
| `net_payable` | = `gross_amount - commission_amount` |
| `settlement_date` | Order date + 7-21 days |
| `settlement_status` | Paid (50%), Processed (25%), Pending (15%), On Hold (10%) |

### Business Rationale

- Only delivered items generate settlements (cancelled/returned items don't)
- Commission rate varies by seller type (Brand Official pays less)
- 7-21 day settlement window is realistic for marketplace payments
- "On Hold" status represents disputed orders or pending return windows

---

## 15. Cross-Table Integrity Rules

These rules ensure the data is consistent across tables:

### Rule 1: Order → Payment (1:1)
Every order has exactly one payment record.

### Rule 2: Order → Shipment (conditional)
Only `Delivered` and `Shipped` orders have shipments.
`Cancelled` and `Processing` orders have NO shipment.

### Rule 3: Order Item → Return (conditional)
Only `Delivered` items with `is_returnable = TRUE` can have returns.

### Rule 4: Return → Refund (conditional)
Only `Completed` returns with `refund_amount > 0` get refunds.

### Rule 5: Order Item → Settlement (conditional)
Only `Delivered` items generate seller settlements.

### Rule 6: Inventory → Movements (multi-source)
Each inventory record gets at least 1 INBOUND movement.
Each order item generates 1 OUTBOUND movement.
Each completed return generates 1 RETURN_INBOUND movement.

### Rule 7: Product → Seller (inherited)
Order items inherit their `seller_id` from the product, NOT randomly.

### Rule 8: Selling Price < MRP (always)
No product has `selling_price >= mrp`.

### Rule 9: Refund Amount ≤ Item Price (always)
No refund exceeds the original item price.

### Rule 10: Foreign Key Insert Order
Tables must be populated in this order:
1.customers
2.sellers
3.warehouses
4.products (depends on sellers)
5.inventory (depends on products, sellers, warehouses)
6.orders (depends on customers)
7.order_items (depends on orders, products, sellers)
8.payments (depends on orders)
9.shipments (depends on orders, warehouses)
10.returns (depends on order_items)
11.refunds (depends on returns)
12.seller_settlements (depends on sellers, order_items)
13.inventory_movements (depends on inventory)


---

## 16. Known Simplifications

These are intentional simplifications made for Stage-1.
They do NOT indicate errors — they are documented trade-offs.

| Simplification | Reason |
|---|---|
| One payment per order | Real systems may have split payments; this keeps it simple |
| One shipment per order | Multi-shipment orders exist but add complexity without insight value |
| No customer addresses table | City/state on customer is sufficient for analysis |
| No coupon/promotion table | Discounts are applied directly on orders |
| No product images/descriptions | Not needed for SQL analytics |
| No real-time inventory sync | Inventory movements approximate reality |
| Warehouse assignment is random | Real systems use proximity-based routing |
| No GST/tax modeling | Tax adds complexity without analytical value at this stage |
| Seller names are synthetic | No real business names used |
| All prices in INR only | No multi-currency support needed |

---

## 17. Validation Checklist

After population, verify these conditions:

- [ ] All foreign keys resolve (no orphan records)
- [ ] `selling_price < mrp` for every product
- [ ] Returns only exist for `Delivered` items
- [ ] Refunds only exist for `Completed` returns
- [ ] Shipments don't exist for `Cancelled` orders
- [ ] COD split is approximately 35%
- [ ] Footwear return rate is highest
- [ ] Top 20% sellers have disproportionate product count
- [ ] No NULL values in primary keys
- [ ] Total row count is approximately 85,000-95,000

---

## 18. Reproducibility

- All generators use `random.seed(42)` and `Faker.seed(42)`
- Running the population script twice (after clearing) produces identical data
- This enables consistent testing and benchmarking

---

*Last updated: Stage-1 Dataset Design & Population*
*Author: Enterprise Decision Copilot Team*