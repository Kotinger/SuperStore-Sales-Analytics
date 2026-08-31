-- clean уже в таблице clean_orders. здесь people слой

USE superstore;

CREATE OR REPLACE VIEW people_orders AS
SELECT * FROM clean_orders WHERE customer_key IS NOT NULL;

CREATE OR REPLACE VIEW customer_agg AS
SELECT
customer_key AS client_id,
COUNT(DISTINCT order_key) AS orders,
SUM(sales) AS gmv,
MIN(DATE(order_date)) AS first_order
FROM people_orders
GROUP BY customer_key;
