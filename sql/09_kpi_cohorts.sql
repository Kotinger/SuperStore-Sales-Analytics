-- когорты + period_n

USE superstore;

WITH order_month AS (
SELECT
customer_key,
order_key,
DATE_FORMAT(MIN(order_date), '%Y-%m-01') AS order_month
FROM people_orders
GROUP BY customer_key, order_key
),
first_cohort AS (
SELECT customer_key, MIN(order_month) AS cohort_month
FROM order_month
GROUP BY customer_key
),
labeled AS (
SELECT
o.customer_key,
f.cohort_month,
PERIOD_DIFF(
DATE_FORMAT(o.order_month, '%Y%m'),
DATE_FORMAT(f.cohort_month, '%Y%m')
) AS period_n
FROM order_month o
INNER JOIN first_cohort f ON f.customer_key = o.customer_key
)
SELECT
cohort_month,
period_n,
COUNT(DISTINCT customer_key) AS customers
FROM labeled
GROUP BY cohort_month, period_n
ORDER BY cohort_month, period_n
LIMIT 200;
