-- STANDARD
-- 2)
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
LEFT JOIN `bigquery-public-data.thelook_ecommerce.users` As u
ON oi.user_id = u.id;

-- 3)
SELECT
  CONCAT (u.first_name, ' ', u.last_name) as full_name,
  COUNT(order_id) AS cnt_order
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
LEFT JOIN `bigquery-public-data.thelook_ecommerce.users` As u
ON oi.user_id = u.id
GROUP BY full_name
ORDER BY cnt_order DESC;

-- 4)
SELECT
  CONCAT (u.first_name, ' ', u.last_name) as full_name,
  COUNT(oi.order_id) AS cnt_order
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
LEFT JOIN `bigquery-public-data.thelook_ecommerce.users` As u
ON oi.user_id = u.id
GROUP BY full_name
HAVING cnt_order >= 3
ORDER BY cnt_order DESC;

-- I have 25080 people

-- 6)
SELECT
  oi.status,
  COUNT(CASE WHEN u.age < 20 THEN oi.order_id END) AS under20,
  COUNT(CASE WHEN u.age >=20 AND u.age <40 THEN oi.order_id END) AS age20_39,
  COUNT(CASE WHEN u.age >=40 AND u.age <60 THEN oi.order_id END) AS age40_59,
  COUNT(CASE WHEN u.age >=60 AND u.age <80 THEN oi.order_id END) AS age60_79,
  COUNT(CASE WHEN u.age >=80 THEN oi.order_id END) AS over80
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
LEFT JOIN `bigquery-public-data.thelook_ecommerce.users` As u
ON oi.user_id = u.id
GROUP BY oi.status;

-- ADVANCED
-- 1)
SELECT
  p.id,
  p.name,
  AVG(ABS(oi.sale_price - p.cost)) AS avg_margin
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
LEFT JOIN `bigquery-public-data.thelook_ecommerce.products` As p
ON oi.product_id = p.id
GROUP BY p.id, p.name
ORDER BY avg_margin DESC
LIMIT 3;

-- 2)
SELECT *
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.products` As p
ON oi.product_id = p.id
JOIN `bigquery-public-data.thelook_ecommerce.users` As u
ON oi.user_id = u.id;

-- 3)
SELECT
  DISTINCT CONCAT (u.first_name, ' ', u.last_name) as full_name,
  ROUND(AVG(ABS(oi.sale_price - p.cost)),2) AS avg_margin
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.products` As p
ON oi.product_id = p.id
JOIN `bigquery-public-data.thelook_ecommerce.users` As u
ON oi.user_id = u.id
GROUP BY full_name
ORDER BY avg_margin DESC
LIMIT 50;

-- 4)
SELECT
  DISTINCT CONCAT (u.first_name, ' ', u.last_name) as full_name,
  COUNT(oi.order_id) AS cnt_orders,
  ROUND(AVG(ABS(oi.sale_price - p.cost)),2) AS avg_margin
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
JOIN `bigquery-public-data.thelook_ecommerce.products` As p
ON oi.product_id = p.id
JOIN `bigquery-public-data.thelook_ecommerce.users` As u
ON oi.user_id = u.id
GROUP BY full_name
HAVING cnt_orders >= 4
ORDER BY avg_margin DESC, cnt_orders DESC
LIMIT 50;

--> Joshua Harris

-- 5)
SELECT
  city,
  STRING_AGG(CONCAT(first_name, ' ', last_name), ', ') AS people,
  COUNT(*) AS total_pop,
  COUNTIF(TRIM(gender) = 'M') AS male_pop,
  COUNTIF(TRIM(gender) = 'F') AS female_pop
FROM `bigquery-public-data.thelook_ecommerce.users`
WHERE TRIM(city) != 'null'
GROUP BY city;