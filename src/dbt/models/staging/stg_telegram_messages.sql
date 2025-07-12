{{ config(materialized='table') }}

SELECT
    (raw_json ->> 'id')::INT AS message_id,
    (raw_json ->> 'message') AS message_text,
    (raw_json ->> 'date')::TIMESTAMP AS message_date,
    COALESCE((raw_json -> 'from_id' ->> 'user_id')::INT, -1) AS sender_id,
    channel
FROM public.raw_telegram_messages
WHERE message_text IS NOT NULL