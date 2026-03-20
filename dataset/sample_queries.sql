-- 1. Row counts for all tables
SELECT 'customers' as tbl, COUNT(*) FROM customers
UNION ALL SELECT 'sellers', COUNT(*) FROM sellers
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'warehouses', COUNT(*) FROM warehouses
UNION ALL SELECT 'inventory', COUNT(*) FROM inventory
UNION ALL SELECT 'inventory_movements', COUNT(*) FROM inventory_movements
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL SELECT 'payments', COUNT(*) FROM payments
UNION ALL SELECT 'shipments', COUNT(*) FROM shipments
UNION ALL SELECT 'returns', COUNT(*) FROM returns
UNION ALL SELECT 'refunds', COUNT(*) FROM refunds
UNION ALL SELECT 'seller_settlements', COUNT(*) FROM seller_settlements
ORDER BY tbl;

-- 2. Verify return rate by category
SELECT p.category, 
       COUNT(DISTINCT oi.order_item_id) as total_delivered,
       COUNT(DISTINCT r.return_id) as total_returned,
       ROUND(COUNT(DISTINCT r.return_id)::numeric / 
             NULLIF(COUNT(DISTINCT oi.order_item_id), 0) * 100, 1) as return_rate_pct
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
LEFT JOIN returns r ON oi.order_item_id = r.order_item_id
WHERE oi.item_status = 'Delivered'
GROUP BY p.category
ORDER BY return_rate_pct DESC;

-- 3. Verify COD vs Prepaid split
SELECT payment_mode, COUNT(*), 
       ROUND(COUNT(*)::numeric / SUM(COUNT(*)) OVER() * 100, 1) as pct
FROM orders
GROUP BY payment_mode;

-- 4. Top 5 sellers by revenue
SELECT s.seller_name, s.seller_type, s.risk_flag,
       SUM(oi.item_price) as total_revenue,
       COUNT(DISTINCT oi.order_item_id) as items_sold
FROM order_items oi
JOIN sellers s ON oi.seller_id = s.seller_id
WHERE oi.item_status = 'Delivered'
GROUP BY s.seller_id, s.seller_name, s.seller_type, s.risk_flag
ORDER BY total_revenue DESC
LIMIT 5;