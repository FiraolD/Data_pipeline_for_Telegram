#telegram.py
from dagster import op
import subprocess

@op
def scrape_telegram_data():
    """Run Telegram scraper to collect new messages and images"""
    result = subprocess.run(["python", "src/scraper/telegram_scraper.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Scraping failed: {result.stderr}")
    return "Scraped data from Telegram"