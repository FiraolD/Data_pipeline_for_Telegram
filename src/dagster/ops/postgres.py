from dagster import op
import subprocess

@op
def load_raw_to_postgres(context, _input):
    context.log.info("Loading raw data into PostgreSQL...")
    result = subprocess.run(["python", "src/db/load_raw_data.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Loading failed: {result.stderr}")
    return "Loaded raw data into Postgres"