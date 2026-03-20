-- ============================================================
-- SCHEMA: Myntra-like E-Commerce Enterprise Dataset
-- Database: PostgreSQL (Supabase)
-- Tables: 13
-- ============================================================
-- Run this top-to-bottom in Supabase SQL Editor.
-- To reset, uncomment the DROP section below and run first.
-- ============================================================

-- ┌──────────────────────────────────────────────────────────┐
-- │  DROP TABLES (uncomment only if you need to reset)       │
-- └──────────────────────────────────────────────────────────┘

-- DROP TABLE IF EXISTS seller_settlements CASCADE;
-- DROP TABLE IF EXISTS refunds CASCADE;
-- DROP TABLE IF EXISTS returns CASCADE;
-- DROP TABLE IF EXISTS shipments CASCADE;
-- DROP TABLE IF EXISTS payments CASCADE;
-- DROP TABLE IF EXISTS order_items CASCADE;
-- DROP TABLE IF EXISTS orders CASCADE;
-- DROP TABLE IF EXISTS inventory_movements CASCADE;
-- DROP TABLE IF EXISTS inventory CASCADE;
-- DROP TABLE IF EXISTS warehouses CASCADE;
-- DROP TABLE IF EXISTS products CASCADE;
-- DROP TABLE IF EXISTS sellers CASCADE;
-- DROP TABLE IF EXISTS customers CASCADE;


-- ┌──────────────────────────────────────────────────────────┐
-- │  1. CUSTOMERS                                            │
-- │  No foreign keys – independent table                     │
-- └──────────────────────────────────────────────────────────┘

CREATE TABLE customers (
  customer_id           VARCHAR PRIMARY KEY,
  signup_date           DATE NOT NULL,
  city                  VARCHAR,
  state                 VARCHAR,
  gender                VARCHAR,
  age_group             VARCHAR,
  loyalty_tier          VARCHAR,
  preferred_payment_mode VARCHAR,
  risk_score            INT,
  is_active             BOOLEAN DEFAULT TRUE
);


-- ┌──────────────────────────────────────────────────────────┐
-- │  2. SELLERS                                              │
-- │  No foreign keys – independent table                     │
-- └──────────────────────────────────────────────────────────┘

CREATE TABLE sellers (
  seller_id       VARCHAR PRIMARY KEY,
  seller_name     VARCHAR,
  seller_type     VARCHAR,
  onboarding_date DATE,
  seller_rating   NUMERIC(2,1),
  seller_region   VARCHAR,
  commission_rate NUMERIC(5,2),
  risk_flag       VARCHAR,
  is_active       BOOLEAN DEFAULT TRUE
);


-- ┌──────────────────────────────────────────────────────────┐
-- │  3. PRODUCTS                                             │
-- │  FK → sellers                                            │
-- └──────────────────────────────────────────────────────────┘

CREATE TABLE products (
  product_id    VARCHAR PRIMARY KEY,
  seller_id     VARCHAR REFERENCES sellers(seller_id),
  brand         VARCHAR,
  category      VARCHAR,
  sub_category  VARCHAR,
  size          VARCHAR,
  color         VARCHAR,
  mrp           NUMERIC(10,2),
  selling_price NUMERIC(10,2),
  season        VARCHAR,
  is_returnable BOOLEAN DEFAULT TRUE
);


-- ┌──────────────────────────────────────────────────────────┐
-- │  4. WAREHOUSES                                           │
-- │  No foreign keys – independent table                     │
-- └──────────────────────────────────────────────────────────┘

CREATE TABLE warehouses (
  warehouse_id    VARCHAR PRIMARY KEY,
  warehouse_city  VARCHAR,
  warehouse_state VARCHAR,
  warehouse_type  VARCHAR,
  is_active       BOOLEAN DEFAULT TRUE
);


-- ┌──────────────────────────────────────────────────────────┐
-- │  5. INVENTORY                                            │
-- │  FK → products, sellers, warehouses                      │
-- └──────────────────────────────────────────────────────────┘

CREATE TABLE inventory (
  inventory_id  VARCHAR PRIMARY KEY,
  product_id    VARCHAR REFERENCES products(product_id),
  seller_id     VARCHAR REFERENCES sellers(seller_id),
  warehouse_id  VARCHAR REFERENCES warehouses(warehouse_id),
  available_qty INT,
  reserved_qty  INT,
  damaged_qty   INT,
  last_updated  TIMESTAMP
);


-- ┌──────────────────────────────────────────────────────────┐
-- │  6. INVENTORY MOVEMENTS                                  │
-- │  FK → inventory                                          │
-- └──────────────────────────────────────────────────────────┘

CREATE TABLE inventory_movements (
  movement_id   VARCHAR PRIMARY KEY,
  inventory_id  VARCHAR REFERENCES inventory(inventory_id),
  movement_type VARCHAR,
  quantity      INT,
  reference_id  VARCHAR,
  movement_date TIMESTAMP
);


-- ┌──────────────────────────────────────────────────────────┐
-- │  7. ORDERS                                               │
-- │  FK → customers                                          │
-- └──────────────────────────────────────────────────────────┘

CREATE TABLE orders (
  order_id        VARCHAR PRIMARY KEY,
  customer_id     VARCHAR REFERENCES customers(customer_id),
  order_date      DATE,
  order_status    VARCHAR,
  payment_mode    VARCHAR,
  total_amount    NUMERIC(10,2),
  discount_amount NUMERIC(10,2),
  final_payable   NUMERIC(10,2),
  order_channel   VARCHAR
);


-- ┌──────────────────────────────────────────────────────────┐
-- │  8. ORDER ITEMS                                          │
-- │  FK → orders, products, sellers                          │
-- └──────────────────────────────────────────────────────────┘

CREATE TABLE order_items (
  order_item_id VARCHAR PRIMARY KEY,
  order_id      VARCHAR REFERENCES orders(order_id),
  product_id    VARCHAR REFERENCES products(product_id),
  seller_id     VARCHAR REFERENCES sellers(seller_id),
  quantity      INT,
  item_price    NUMERIC(10,2),
  item_status   VARCHAR
);


-- ┌──────────────────────────────────────────────────────────┐
-- │  9. PAYMENTS                                             │
-- │  FK → orders                                             │
-- └──────────────────────────────────────────────────────────┘

CREATE TABLE payments (
  payment_id     VARCHAR PRIMARY KEY,
  order_id       VARCHAR REFERENCES orders(order_id),
  payment_method VARCHAR,
  payment_status VARCHAR,
  payment_date   TIMESTAMP,
  paid_amount    NUMERIC(10,2),
  gateway        VARCHAR
);


-- ┌──────────────────────────────────────────────────────────┐
-- │  10. SHIPMENTS                                           │
-- │  FK → orders, warehouses                                 │
-- └──────────────────────────────────────────────────────────┘

CREATE TABLE shipments (
  shipment_id           VARCHAR PRIMARY KEY,
  order_id              VARCHAR REFERENCES orders(order_id),
  warehouse_id          VARCHAR REFERENCES warehouses(warehouse_id),
  courier_partner       VARCHAR,
  shipped_date          DATE,
  promised_delivery_date DATE,
  actual_delivery_date  DATE,
  delivery_status       VARCHAR
);


-- ┌──────────────────────────────────────────────────────────┐
-- │  11. RETURNS                                             │
-- │  FK → order_items                                        │
-- └──────────────────────────────────────────────────────────┘

CREATE TABLE returns (
  return_id     VARCHAR PRIMARY KEY,
  order_item_id VARCHAR REFERENCES order_items(order_item_id),
  return_date   DATE,
  return_reason VARCHAR,
  return_type   VARCHAR,
  return_status VARCHAR,
  pickup_date   DATE,
  refund_amount NUMERIC(10,2)
);


-- ┌──────────────────────────────────────────────────────────┐
-- │  12. REFUNDS                                             │
-- │  FK → returns                                            │
-- └──────────────────────────────────────────────────────────┘

CREATE TABLE refunds (
  refund_id       VARCHAR PRIMARY KEY,
  return_id       VARCHAR REFERENCES returns(return_id),
  refund_method   VARCHAR,
  refund_status   VARCHAR,
  refund_date     DATE,
  refunded_amount NUMERIC(10,2)
);


-- ┌──────────────────────────────────────────────────────────┐
-- │  13. SELLER SETTLEMENTS                                  │
-- │  FK → sellers, order_items                               │
-- └──────────────────────────────────────────────────────────┘

CREATE TABLE seller_settlements (
  settlement_id     VARCHAR PRIMARY KEY,
  seller_id         VARCHAR REFERENCES sellers(seller_id),
  order_item_id     VARCHAR REFERENCES order_items(order_item_id),
  gross_amount      NUMERIC(10,2),
  commission_amount NUMERIC(10,2),
  net_payable       NUMERIC(10,2),
  settlement_date   DATE,
  settlement_status VARCHAR
);


-- ┌──────────────────────────────────────────────────────────┐
-- │  INDEXES (run after all tables are created)              │
-- └──────────────────────────────────────────────────────────┘

CREATE INDEX idx_orders_customer    ON orders(customer_id);
CREATE INDEX idx_orders_date        ON orders(order_date);
CREATE INDEX idx_order_items_order  ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
CREATE INDEX idx_products_seller    ON products(seller_id);
CREATE INDEX idx_inventory_product  ON inventory(product_id);
CREATE INDEX idx_inventory_warehouse ON inventory(warehouse_id);
CREATE INDEX idx_returns_order_item ON returns(order_item_id);
CREATE INDEX idx_shipments_order    ON shipments(order_id);
CREATE INDEX idx_settlements_seller ON seller_settlements(seller_id);