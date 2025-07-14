{{ config(materialized='table') }}

-- Extract channel metadata from raw messages
WITH channel_data AS (
    SELECT DISTINCT
        channel AS channel_name,
        NOW() AS extracted_at
    FROM {{ source('raw', 'telegram_messages') }}
)

SELECT
    channel_name,
    extracted_at
FROM channel_data