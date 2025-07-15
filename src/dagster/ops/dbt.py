import os
from dagster import op
import subprocess

@op
def run_dbt_transformations(context, _input):
    context.log.info("Running dbt transformations...")
    result = subprocess.run(["cd", "src/dbt", "&&", "dbt", "--profile", "telegram_dw", "run"], shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"dbt run failed: {result.stderr}")
    context.log.info("dbt models built successfully")
    return "dbt models built"