-- срез по стране

USE superstore;

SELECT
country,
SUM(sales) AS gmv,
COUNT(DISTINCT order_key) AS orders,
COUNT(*) AS lines,
SUM(sales) / COUNT(DISTINCT order_key) AS aov
FROM clean_orders
GROUP BY country
ORDER BY gmv DESC
LIMIT 10;
