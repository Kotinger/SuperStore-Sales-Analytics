-- margin и топ товаров (маршрут C)

USE superstore;

SELECT
category,
SUM(sales) AS sales,
SUM(profit) AS profit,
SUM(profit) / SUM(sales) AS margin_pct
FROM clean_orders
GROUP BY category
ORDER BY margin_pct DESC;

SELECT
product_name,
SUM(sales) AS gmv,
COUNT(DISTINCT order_key) AS orders
FROM clean_orders
GROUP BY product_name
ORDER BY gmv DESC
LIMIT 10;
