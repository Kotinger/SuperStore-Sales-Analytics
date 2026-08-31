-- repeat + ltv. ожидаемо: customers 15700, repeat ~30.4%

USE superstore;

SELECT
COUNT(*) AS customers,
AVG(CASE WHEN orders >= 2 THEN 1 ELSE 0 END) AS repeat_rate,
AVG(gmv) AS ltv_avg,
SUM(gmv) / COUNT(*) AS ltv_mean_check
FROM people;

SELECT
COUNT(*) AS customers,
AVG(CASE WHEN orders >= 2 THEN 1 ELSE 0 END) AS repeat_rate,
AVG(gmv) AS ltv_avg
FROM customer_agg;
