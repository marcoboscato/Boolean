-- STANDARD --

-- 1)

SELECT
  PLANT,
  ROUND(AVG(AC_POWER),2) AS avg_ac,
  ROUND(AVG(DC_POWER),2) AS avg_dc
FROM `sql-sandbox-boolean-488922.SolarPower.Generation_Data`
GROUP BY PLANT

-- 2)

WITH inverter AS (
  SELECT
    PLANT,
    SOURCE_KEY,
  ROUND(AVG(AC_POWER/(DC_POWER+1e-5)),3) AS avg_dc_to_ac_ratio,
  FROM `sql-sandbox-boolean-488922.SolarPower.Generation_Data`
  GROUP BY PLANT, SOURCE_KEY
)

SELECT
  PLANT,
  ROUND(AVG(avg_dc_to_ac_ratio),3) AS total_avg,
FROM inverter
GROUP BY PLANT

-- 3): The second pannel is a lot more performative. The first seems to have some issues

-- 4)

WITH inverter AS (
  SELECT
    DATE_TIME,
    AVG(DC_POWER) AS avg_dc_power,
    AVG(AC_POWER) AS avg_ac_power
  FROM `sql-sandbox-boolean-488922.SolarPower.Generation_Data`
  WHERE PLANT = 1
  GROUP BY DATE_TIME
  ORDER BY DATE_TIME ASC
)

SELECT
  HOUR_INTERVAL,
  sum_avg_dc_power,
  sum_avg_ac_power,
  ROUND(sum_avg_ac_power/(sum_avg_dc_power + 1e-3),2) as ac_dc_ration
FROM ( 
      SELECT
        TIMESTAMP_TRUNC(DATE_TIME, HOUR) AS HOUR_INTERVAL,
        SUM(avg_dc_power) AS sum_avg_dc_power,
        SUM(avg_ac_power) AS sum_avg_ac_power
      FROM inverter
      GROUP BY HOUR_INTERVAL
      ORDER BY HOUR_INTERVAL ASC
);

-- 5): simply the zeros means night hours

-- 6)

SELECT
  PLANT,
  COUNT(DISTINCT SOURCE_KEY) AS cnt_inverter
FROM `sql-sandbox-boolean-488922.SolarPower.Generation_Data`
GROUP BY PLANT
ORDER BY PLANT ASC;

SELECT
  PLANT,
  COUNT(DISTINCT SOURCE_KEY) AS cnt_inverter
FROM `sql-sandbox-boolean-488922.SolarPower.Weather_Sensor_Data`
GROUP BY PLANT
ORDER BY PLANT ASC;

-- 7)

SELECT *
FROM `sql-sandbox-boolean-488922.SolarPower.Generation_Data` as gd
INNER JOIN `sql-sandbox-boolean-488922.SolarPower.Weather_Sensor_Data` as wsd ON gd.SOURCE_KEY = wsd.SOURCE_KEY
ORDER BY gd.PLANT

-- or

SELECT *
FROM `sql-sandbox-boolean-488922.SolarPower.Generation_Data`
WHERE TRIM(SOURCE_KEY) = 'iq8k7ZNt4Mwm3w0' OR TRIM(SOURCE_KEY) = 'HmiyD2TTLFNqkNe'
ORDER BY PLANT


--> BUT NO DATA!

-- 8)

UPDATE `sql-sandbox-boolean-488922.SolarPower.Generation_Data`
SET DC_POWER = DC_POWER / 10
WHERE PLANT = 1;


-- ADVANCED --

-- 1)

CREATE TABLE `sql-sandbox-boolean-488922.SolarPower.Generation_Data_corrected` AS
SELECT
  DATE_TIME,
  SOURCE_KEY,
  DC_POWER / 10 AS DC_POWER,
  AC_POWER,
  DAILY_YIELD,
  TOTAL_YIELD,
  PLANT
FROM `sql-sandbox-boolean-488922.SolarPower.Generation_Data`
ORDER BY DATE_TIME,PLANT;