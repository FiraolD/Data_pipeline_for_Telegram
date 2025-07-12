{{ config(materialized='table') }}

SELECT
    msg.message_id,
    msg.message_text,
    msg.message_date,
    msg.sender_id,
    dc.channel_key,
    dd.date_day
FROM {{ ref('stg_telegram_messages') }} msg
LEFT JOIN {{ ref('dim_channels') }} dc ON msg.channel = dc.channel_name
LEFT JOIN {{ ref('dim_dates') }} dd ON msg.message_date::DATE = dd.date_day