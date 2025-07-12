{{ config(materialized='table') }}

WITH date_spine AS (
    SELECT generate_series(
        (SELECT MIN(message_date) FROM {{ ref('stg_telegram_messages') }},
        (SELECT MAX(message_date) FROM {{ ref('stg_telegram_messages') }},
        '1 day'
    )::DATE AS date_day
)
SELECT
    date_day,
    EXTRACT(YEAR FROM date_day) AS year,
    EXTRACT(MONTH FROM date_day) AS month,
    EXTRACT(DAY FROM date_day) AS day,
    TO_CHAR(date_day, 'Day') AS day_of_week
FROM date_spine