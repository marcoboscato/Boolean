-- UNION

CREATE TABLE `sql-sandbox-boolean-488922.SolarPower.Generation_Data` AS
SELECT
  DATE_TIME,
  SOURCE_KEY,
  DC_POWER,
  AC_POWER,
  DAILY_YIELD,
  TOTAL_YIELD,
  CASE WHEN PLANT_ID = 4135001 THEN 1 END AS PLANT    
FROM `sql-sandbox-boolean-488922.SolarPower.Plant_1_Generation_Data`
UNION ALL
SELECT
  DATE_TIME,
  SOURCE_KEY,
  DC_POWER,
  AC_POWER,
  DAILY_YIELD,
  TOTAL_YIELD,
  CASE WHEN PLANT_ID = 4136001 THEN 2 END AS PLANT
FROM `sql-sandbox-boolean-488922.SolarPower.Plant_2_Generation_Data`;


CREATE TABLE `sql-sandbox-boolean-488922.SolarPower.Weather_Sensor_Data` AS
SELECT
  DATE_TIME,
  SOURCE_KEY,
  AMBIENT_TEMPERATURE,
  MODULE_TEMPERATURE,
  IRRADIATION,
  CASE WHEN PLANT_ID = 4135001 THEN 1 END AS PLANT    
FROM `sql-sandbox-boolean-488922.SolarPower.Plant_1_Weather_Sensor_Data`
UNION ALL
SELECT
  DATE_TIME,
  SOURCE_KEY,
  AMBIENT_TEMPERATURE,
  MODULE_TEMPERATURE,
  IRRADIATION,
  CASE WHEN PLANT_ID = 4136001 THEN 2 END AS PLANT
FROM `sql-sandbox-boolean-488922.SolarPower.Plant_2_Weather_Sensor_Data`;

-- 5)

SELECT
  PLANT,
  COUNT(SOURCE_KEY) AS cnt_source_key
FROM `sql-sandbox-boolean-488922.SolarPower.Generation_Data`
GROUP BY PLANT
ORDER BY PLANT ASC;

SELECT
  PLANT,
  COUNT(SOURCE_KEY) AS cnt_source_key
FROM `sql-sandbox-boolean-488922.SolarPower.Weather_Sensor_Data`
GROUP BY PLANT
ORDER BY PLANT ASC;

-- 6)

SELECT
  PLANT,
  COUNT(DISTINCT DATE(DATE_TIME)) AS simple_date
FROM `sql-sandbox-boolean-488922.SolarPower.Generation_Data`
GROUP BY PLANT;

SELECT
  PLANT,
  COUNT(DISTINCT DATE(DATE_TIME)) AS simple_date
FROM `sql-sandbox-boolean-488922.SolarPower.Weather_Sensor_Data`
GROUP BY PLANT;

-- 7)

WITH base AS (
  SELECT
    DATE_TIME,
    SOURCE_KEY,
    PLANT,
    -- substract the first total yield valued at the beginning of the measuraments and sum for each key
    TOTAL_YIELD - FIRST_VALUE(TOTAL_YIELD) OVER (PARTITION BY SOURCE_KEY ORDER BY DATE_TIME) AS yield_delta
  FROM `sql-sandbox-boolean-488922.SolarPower.Generation_Data`
)

SELECT
  SOURCE_KEY,
  SUM(yield_delta) AS total_yield,
  -- retrive the floor where each inverter is located
  CAST(SUM(PLANT) / COUNT(PLANT) AS int) AS plant
FROM base
GROUP BY SOURCE_KEY
ORDER BY total_yield DESC


--- DATA DEFINITION LANGUAGE ---

-- 1) and 2)

CREATE TABLE students(
  id INTEGER PRIMARY KEY,
  nmStudent VARCHAR(255) NOT NULL,
  idCourse INT
  );
  
 CREATE TABLE courses(
  id INTEGER PRIMARY KEY,
  nmCourse VARCHAR(255) NOT NULL
  );
  
INSERT INTO students(nmstudent, idcourse)
VALUES
  	('Mark', 1),
  	('Jack', 2),
    ('Ivan', 3),
    ('Beth', 3),
	('Sara', 5);
    
SELECT * FROM students;
  
INSERT INTO courses(nmcourse)
VALUES
  	('Math'),
  	('English'),
    ('Physics'),
    ('Business'),
	('History');

SELECT * FROM courses;

-- 3)

SELECT
	s.nmStudent,
    c.nmCourse
FROM students AS s
LEFT JOIN courses AS c ON s.idCourse = c.id;

-- 4)

UPDATE students
SET idcourse = 4
WHERE id = 5;

SELECT * FROM students;

-- 5)

UPDATE courses
SET nmCourse = 'Economics'
WHERE id = 5;

SELECT * FROM courses;

-- 6)

INSERT INTO students (nmstudent, idcourse)
VALUES ('George', 5);

SELECT * FROM students;

-- 7): all the modification are updates when I join the two table since is a relational database


-- ADVANCED --

-- 1)

SELECT oi.*, p.*
FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
LEFT JOIN `bigquery-public-data.thelook_ecommerce.products` As p ON oi.product_id = p.id
LIMIT 50;

-- 2)

WITH product_orders AS ( 
  SELECT oi.*, p.*
  FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.products` As p ON oi.product_id = p.id
)

SELECT
  category,
  COUNT (DISTINCT order_id) AS cnt_orders_x_product
FROM product_orders
GROUP BY category
ORDER BY cnt_orders_x_product DESC;

-- 3)

WITH product_orders AS ( 
  SELECT oi.*, p.*
  FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.products` As p ON oi.product_id = p.id
)

SELECT
  category,
  COUNT (DISTINCT order_id) AS cnt_orders_x_product,
  ROUND (AVG (retail_price - cost), 2) as avg_margin_per_order
  --(SUM(retail_price) - SUM(cost))/count(distinct order_id) as avg_margin_per_order
FROM product_orders
GROUP BY category
ORDER BY avg_margin_per_order DESC;

-- 4)

WITH product_orders AS ( 
  SELECT oi.*, p.*
  FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.products` As p ON oi.product_id = p.id
  WHERE TRIM(oi.status) = 'Complete'
)

SELECT
  name,
  category,
  COUNT (order_id) AS cnt_orders_x_product,
FROM product_orders
GROUP BY name, category
ORDER BY cnt_orders_x_product DESC;

-- 5)

WITH product_orders AS ( 
  SELECT oi.*, p.*
  FROM `bigquery-public-data.thelook_ecommerce.order_items` AS oi
  LEFT JOIN `bigquery-public-data.thelook_ecommerce.products` As p ON oi.product_id = p.id
  WHERE TRIM(oi.status) = 'Complete' AND oi.returned_at IS NULL
)

SELECT
  name,
  delivered_at,
  shipped_at,
  TIMESTAMP_DIFF(delivered_at, shipped_at, MINUTE) AS delta_delivery_minutes
FROM product_orders
ORDER BY delta_delivery_minutes DESC;

-- 6)

SELECT
  name,
  delivered_at,
  shipped_at,
  TIMESTAMP_DIFF(delivered_at, shipped_at, MINUTE) AS delta_delivery_minutes
FROM product_orders
ORDER BY delta_delivery_minutes ASC;