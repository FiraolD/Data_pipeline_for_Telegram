version: 2

models:
    - name: stg_telegram_messages
    description: "Staging table for raw Telegram messages"
    columns:
    - name: message_id
        description: "Unique ID for each message"
        tests:
            - unique
            - not_null

    - name: message_date
        description: "Date the message was sent"
        tests:
            - not_null