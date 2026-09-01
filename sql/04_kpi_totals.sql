-- gmv 12642905, orders 25754, aov ~491, lines 51289

USE superstore;

SELECT
SUM(sales) AS gmv,
COUNT(DISTINCT order_key) AS orders,
COUNT(*) AS `lines`,
SUM(sales) / COUNT(DISTINCT order_key) AS aov
FROM clean_orders;
