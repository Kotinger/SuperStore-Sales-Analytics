-- год x месяц

USE superstore;

SELECT
year,
MONTH(order_date) AS month,
SUM(sales) AS gmv,
COUNT(DISTINCT order_key) AS orders,
SUM(sales) / COUNT(DISTINCT order_key) AS aov
FROM clean_orders
GROUP BY year, MONTH(order_date)
ORDER BY year, month;
