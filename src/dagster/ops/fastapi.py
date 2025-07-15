from dagster import op
import subprocess

@op
def serve_fastapi(context):
    context.log.info("Starting FastAPI server...")
    result = subprocess.run(["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"FastAPI failed to start: {result.stderr}")
    return "FastAPI server running"