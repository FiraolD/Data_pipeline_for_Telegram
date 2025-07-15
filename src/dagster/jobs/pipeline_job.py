
from dagster import job
from src.dagster.ops.telegram import scrape_telegram_data
from src.dagster.ops.postgres import load_raw_to_postgres
from src.dagster.ops.dbt import run_dbt_transformations
from src.dagster.ops.yolo import run_yolo_detection

@job
def run_full_pipeline():
    raw_data = scrape_telegram_data()
    loaded = load_raw_to_postgres(raw_data)
    transformed = run_dbt_transformations(loaded)
    detected = run_yolo_detection(transformed)