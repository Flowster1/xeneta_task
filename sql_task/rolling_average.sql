WITH latest_departures AS (
    SELECT DISTINCT ON (
        "SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS",  
        "ORIGIN_SERVICE_VERSION_AND_MASTER", 
        "DESTINATION_SERVICE_VERSION_AND_MASTER"
    )
        "OFFERED_CAPACITY_TEU"::float AS final_capacity,
        "ORIGIN_AT_UTC"::timestamp AS final_china_departure
    FROM sailing_level
    WHERE "ORIGIN" = 'china_main' 
      AND "DESTINATION" = 'north_europe_main'
      AND "ORIGIN_AT_UTC"::date BETWEEN '2024-01-01' AND '2024-03-31'  
    ORDER BY 
        "SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS", 
        "ORIGIN_SERVICE_VERSION_AND_MASTER", 
        "DESTINATION_SERVICE_VERSION_AND_MASTER",
        "ORIGIN_AT_UTC" DESC
),
weekly_totals AS (
    SELECT 
        DATE_TRUNC('week', final_china_departure)::date AS week_start_date,
        SUM(final_capacity) AS weekly_capacity
    FROM latest_departures
    GROUP BY 1
),
rolling_calculation AS (
    SELECT 
        week_start_date,
        weekly_capacity,
        AVG(weekly_capacity) OVER (
            ORDER BY week_start_date 
            ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
        ) AS rolling_avg
    FROM weekly_totals
)
SELECT 
    week_start_date,
    ROUND(rolling_avg)::integer AS rolling_avg_4week_teu
FROM rolling_calculation
ORDER BY week_start_date;