from dagster import op
import subprocess

@op
def run_yolo_detection(context, _input):
    context.log.info("Running YOLO detection on downloaded images...")
    result = subprocess.run(["python", "src/yolo/detector.py"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"YOLO detection failed: {result.stderr}")
    context.log.info("Image detections saved to database")
    return "YOLO detection completed"