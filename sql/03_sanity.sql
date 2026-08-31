-- ожидаемо: rows 51289, orders 25754, gmv 12642905

USE superstore;

SELECT COUNT(*) AS rows_n FROM clean_orders;

SELECT
COUNT(DISTINCT order_key) AS orders_n,
SUM(sales) AS gmv,
MIN(order_date) AS date_min,
MAX(order_date) AS date_max
FROM clean_orders;

SELECT COUNT(*) AS people_n FROM people;
