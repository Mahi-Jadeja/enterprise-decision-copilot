#!/usr/bin/env python3
"""
populate_supabase.py
====================
Main orchestrator script for Stage-1 data population.

Run this AFTER schema.sql has been executed in Supabase.

Usage:
    cd dataset/
    python populate_supabase.py

Prerequisites:
    - PostgreSQL tables created via schema.sql
    - .env file configured in config/.env
    - pip install psycopg2-binary faker python-dotenv
"""

import sys
import os

# Add parent directory to path so we can import helpers/ and generators/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from helpers.db import get_connection, insert_batch, test_connection
import psycopg2.extras


def fetch_all(conn, table):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f"SELECT * FROM {table};")
    rows = cur.fetchall()
    cur.close()
    return rows

# Import all generators
from generators.gen_customers import generate_customers, CUSTOMERS_COLUMNS
from generators.gen_sellers import generate_sellers, SELLERS_COLUMNS
from generators.gen_products import generate_products, PRODUCTS_COLUMNS
from generators.gen_warehouses import generate_warehouses, WAREHOUSES_COLUMNS
from generators.gen_inventory import generate_inventory, INVENTORY_COLUMNS
from generators.gen_orders import (
    generate_orders_and_items, ORDERS_COLUMNS, ORDER_ITEMS_COLUMNS
)
from generators.gen_payments import generate_payments, PAYMENTS_COLUMNS
from generators.gen_shipments import generate_shipments, SHIPMENTS_COLUMNS
from generators.gen_returns import generate_returns, RETURNS_COLUMNS
from generators.gen_refunds import generate_refunds, REFUNDS_COLUMNS
from generators.gen_seller_settlements import (
    generate_seller_settlements, SELLER_SETTLEMENTS_COLUMNS
)
from generators.gen_inventory_movements import (
    generate_inventory_movements, INVENTORY_MOVEMENTS_COLUMNS
)


def clear_tables(conn):
    """Delete all data from tables in reverse dependency order."""
    tables_in_order = [
        "seller_settlements",
        "refunds",
        "returns",
        "inventory_movements",
        "shipments",
        "payments",
        "order_items",
        "orders",
        "inventory",
        "warehouses",
        "products",
        "sellers",
        "customers",
    ]
    cursor = conn.cursor()
    for table in tables_in_order:
        cursor.execute(f"DELETE FROM {table};")
        print(f"  🗑 Cleared {table}")
    conn.commit()
    cursor.close()
    print()


def main():
    print("=" * 60)
    print("  STAGE-1: Enterprise Dataset Population")
    print("  Myntra-like E-Commerce Decision Copilot")
    print("=" * 60)
    print()

    # ── Step 0: Test connection ──
    print("🔌 Testing database connection...")
    if not test_connection():
        print("❌ Cannot connect to database. Check your .env file.")
        sys.exit(1)
    print()

    conn = get_connection()
    print("🔄 Reloading existing data from database...")

    customers = fetch_all(conn, "customers")
    sellers = fetch_all(conn, "sellers")
    seller_ids = [s[0] for s in sellers]
    warehouses = fetch_all(conn, "warehouses")
    warehouse_ids = [w[0] for w in warehouses]
    products = fetch_all(conn, "products")
    inventory = fetch_all(conn, "inventory")
    

    print("✅ Reload complete")
    print()
    
    
    # ── Step 0.5: Clear existing data ──
    #print("🧹 Clearing existing data...")
    #clear_tables(conn)

    # ══════════════════════════════════════════════
    # PHASE 1: Independent tables (no FK dependencies)
    # ══════════════════════════════════════════════

    # ── Step 1: Customers ──
   #print("👥 Generating customers...")
    #customers = generate_customers()
    #insert_batch(conn, "customers", CUSTOMERS_COLUMNS, customers)

    # ── Step 2: Sellers ──
    #print("🏪 Generating sellers...")
    #sellers = generate_sellers()
    #insert_batch(conn, "sellers", SELLERS_COLUMNS, sellers)

    # ── Step 3: Warehouses ──
    #print("🏭 Generating warehouses...")
    #warehouses = generate_warehouses()
    #insert_batch(conn, "warehouses", WAREHOUSES_COLUMNS, warehouses)

    # ══════════════════════════════════════════════
    # PHASE 2: Tables dependent on Phase 1
    # ══════════════════════════════════════════════

    # ── Step 4: Products (depends on sellers) ──
    #print("📦 Generating products...")
    #seller_ids = [s[0] for s in sellers]
    #products = generate_products(seller_ids)
    #insert_batch(conn, "products", PRODUCTS_COLUMNS, products)

    # ── Step 5: Inventory (depends on products, sellers, warehouses) ──
    #print("📊 Generating inventory...")
    #warehouse_ids = [w[0] for w in warehouses]
    #inventory = generate_inventory(products, warehouse_ids)
    #insert_batch(conn, "inventory", INVENTORY_COLUMNS, inventory)  

    # ══════════════════════════════════════════════
    # PHASE 3: Orders & Order Items
    # ══════════════════════════════════════════════

    # ── Step 6: Orders & Order Items ──
    
    print("🛒 Generating orders and order items...")
    customer_ids = [c[0] for c in customers]
    orders, order_items = generate_orders_and_items(
        customer_ids, products, seller_ids
    )
    insert_batch(conn, "orders", ORDERS_COLUMNS, orders)
    insert_batch(conn, "order_items", ORDER_ITEMS_COLUMNS, order_items)

    # ══════════════════════════════════════════════
    # PHASE 4: Post-order tables
    # ══════════════════════════════════════════════

    # Build lookup dicts needed by downstream generators
    order_lookup = {o[0]: o for o in orders}
    product_lookup = {p[0]: p for p in products}
    seller_lookup = {s[0]: s for s in sellers}

    # Customer city map for shipment logic
    customer_city_map = {c[0]: c[2] for c in customers}

    # ── Step 7: Payments ──
    print("💳 Generating payments...")
    payments = generate_payments(orders)
    insert_batch(conn, "payments", PAYMENTS_COLUMNS, payments)

    # ── Step 8: Shipments ──
    print("🚚 Generating shipments...")
    shipments = generate_shipments(orders, warehouse_ids, customer_city_map)
    insert_batch(conn, "shipments", SHIPMENTS_COLUMNS, shipments)

    # ── Step 9: Returns ──
    print("↩️  Generating returns...")
    returns = generate_returns(
        order_items, order_lookup, product_lookup, seller_lookup
    )
    insert_batch(conn, "returns", RETURNS_COLUMNS, returns)

    # ── Step 10: Refunds ──
    print("💰 Generating refunds...")
    refunds = generate_refunds(returns)
    insert_batch(conn, "refunds", REFUNDS_COLUMNS, refunds)

    # ── Step 11: Seller Settlements ──
    print("🤝 Generating seller settlements...")
    settlements = generate_seller_settlements(
        order_items, order_lookup, seller_lookup
    )
    insert_batch(conn, "seller_settlements", SELLER_SETTLEMENTS_COLUMNS, settlements)

    # ── Step 12: Inventory Movements ──
    print("📋 Generating inventory movements...")
    movements = generate_inventory_movements(inventory, order_items, returns)
    insert_batch(conn, "inventory_movements", INVENTORY_MOVEMENTS_COLUMNS, movements)

    # ══════════════════════════════════════════════
    # DONE
    # ══════════════════════════════════════════════

    conn.close()

    print("=" * 60)
    print("  ✅ STAGE-1 DATA POPULATION COMPLETE!")
    print("=" * 60)
    print()
    print("  Summary:")
    print(f"    Customers:           {len(customers):,}")
    print(f"    Sellers:             {len(sellers):,}")
    print(f"    Products:            {len(products):,}")
    print(f"    Warehouses:          {len(warehouses):,}")
    print(f"    Inventory:           {len(inventory):,}")
    print(f"    Orders:              {len(orders):,}")
    print(f"    Order Items:         {len(order_items):,}")
    print(f"    Payments:            {len(payments):,}")
    print(f"    Shipments:           {len(shipments):,}")
    print(f"    Returns:             {len(returns):,}")
    print(f"    Refunds:             {len(refunds):,}")
    print(f"    Settlements:         {len(settlements):,}")
    print(f"    Inv. Movements:      {len(movements):,}")
    print(f"    ────────────────────────────")
    total = (
        len(customers) + len(sellers) + len(products) + len(warehouses)
        + len(inventory) + len(orders) + len(order_items) + len(payments)
        + len(shipments) + len(returns) + len(refunds) + len(settlements)
        + len(movements)
    )
    print(f"    TOTAL ROWS:          {total:,}")
    print()
    print("  Next steps:")
    print("    1. Run sample_queries.sql to validate")
    print("    2. Check data in Supabase Table Editor")
    print("    3. Freeze Stage-1 ✓")
    print()


if __name__ == "__main__":
    main()