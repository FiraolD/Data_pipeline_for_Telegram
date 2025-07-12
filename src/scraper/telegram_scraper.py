from telethon.sync import TelegramClient
from telethon.tl.types import PeerChannel, MessageMediaPhoto
import os
import json
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Telegram credentialshttps://t.me/CheMed123
api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
phone = os.getenv("TELEGRAM_PHONE")

# List of target channels: {"handle": "channel_id or username"}
channels = {
    "lobelia4cosmetics": "lobelia4cosmetics",
    "tikvahpharma": "tikvahpharma",
    "CheMed123": "CheMed123"
    
}

# Output directories
date_str = datetime.now().strftime("%Y-%m-%d")
raw_data_dir = f"Data/raw/telegram_messages/{date_str}"
image_data_dir = f"Data/raw/images"

os.makedirs(raw_data_dir, exist_ok=True)
os.makedirs(image_data_dir, exist_ok=True)


async def scrape_channel(client, channel_handle, channel_ref):
    try:
        logger.info(f"Scraping channel: {channel_handle}")
        channel = await client.get_entity(channel_ref)
        messages = []

        async for message in client.iter_messages(channel, limit=100):  # Adjust limit
            msg_dict = message.to_dict()
            messages.append(msg_dict)

            # Download image if present
            if isinstance(message.media, MessageMediaPhoto):
                photo_path = os.path.join(image_data_dir, channel_handle)
                os.makedirs(photo_path, exist_ok=True)
                filename = f"{message.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                await client.download_media(message.media, file=os.path.join(photo_path, filename))
                logger.info(f"Downloaded image: {filename}")

        output_path = os.path.join(raw_data_dir, f"{channel_handle}.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=4, default=str)

        logger.info(f"Saved {len(messages)} messages from {channel_handle} to {output_path}")

    except Exception as e:
        logger.error(f"Error scraping {channel_handle}: {str(e)}")


async def main():
    async with TelegramClient('session_name', api_id, api_hash) as client:
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            code = input('Enter the code you received: ')
            await client.sign_in(phone, code)

        for channel_handle, channel_ref in channels.items():
            await scrape_channel(client, channel_handle, channel_ref)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())