{{ config(materialized='table') }}

SELECT
    ROW_NUMBER() OVER () AS channel_key,
    channel AS channel_name,
    NOW() AS effective_date,
    TRUE AS current_flag
FROM (
    SELECT DISTINCT channel FROM {{ ref('stg_telegram_messages') }}
)