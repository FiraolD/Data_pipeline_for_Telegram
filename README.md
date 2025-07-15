  📊 Telegram Data Pipeline

A data pipeline that scrapes public messages and images from Ethiopian medical-related Telegram channels, enriches the data with   YOLOv8   object detection, models it using   dbt  , exposes insights via   FastAPI  , and orchestrates everything with   Dagster  .

   🎯 Project Overview

This project collects data from public Telegram channels related to health and pharmaceuticals in Ethiopia. It transforms and enriches the data using modern tools like   dbt  , detects products in images using   YOLOv8  , and exposes analytical endpoints through   FastAPI  . All steps are orchestrated using   Dagster   for scheduling and observability.

   🧱 Key Components

| Component | Description |
|----------|-------------|
|   Telegram Scraper   | Uses Telethon to scrape messages and images from public Telegram channels |
|   PostgreSQL   | Raw message storage and warehouse foundation |
|   dbt Models   | Staging and marts for dimensional modeling |
|   YOLOv8 Detection   | Detects objects (e.g., bottles, phones) in images |
|   FastAPI   | RESTful API exposing top products, activity trends, and message search |
|   Dagster   | Orchestration engine for full pipeline automation |

   🔁 Tasks Completed

- ✅ Task 0 – Project Setup & Environment Management
- ✅ Task 1 – Telegram Scraping
- ✅ Task 2 – Data Modeling with dbt
- ✅ Task 3 – Data Enrichment with YOLOv8
- ✅ Task 4 – Analytical API with FastAPI
- ✅ Task 5 – Pipeline Orchestration with Dagster

   🚀 Quick Start

    Prerequisites

- Docker installed
- Python 3.11 or higher
- PostgreSQL running locally or via Docker

    1. Clone the repo

```bash
git clone https://github.com/your-username/Data_pipeline_for_Telegram.git
cd Data_pipeline_for_Telegram
```

    2. Set up environment variables

Create `.env` file:

```env
DB_NAME=telegram_dw
DB_USER=postgres
DB_PASSWORD=Fira@0412
DB_HOST=localhost
DB_PORT=5432
```

    3. Build and run with Docker

```bash
docker-compose up --build
```

This starts:
- PostgreSQL database
- FastAPI application
- Dagster orchestration UI

   🛠 Folder Structure

```
Data_pipeline_for_Telegram/
├── src/
│   ├── main.py                   FastAPI entry point
│   ├── telegram/
│   │   └── scraper.py            Telegram scraping logic
│   ├── yolo/
│   │   └── detector.py           YOLOv8 image detection
│   ├── dagster/
│   │   ├── ops/
│   │   │   ├── telegram.py       Dagster op for Telegram scraping
│   │   │   ├── postgres.py       Dagster op for loading raw data
│   │   │   ├── dbt.py            Dagster op for dbt transformations
│   │   │   └── yolo.py          Dagster op for image detection
│   │   └── jobs/
│   │       └── pipeline_job.py   Full pipeline job definition
│   └── api/
│       ├── products.py           Top products endpoint
│       ├── channels.py           Channel activity endpoint
│       └── messages.py           Message search endpoint
├── data/
│   └── raw/
│       └── images/
│           ├── lobelia4cosmetics/
│           ├── tikvahpharma/
│           └── CheMed123/
├── src/dbt/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   │       ├── fct_messages.sql
│   │       └── fct_image_detections.sql
│   │       └── dim_channels.sql
│   │       └── dim_dates.sql
│   └── dbt_project.yml
├── requirements.txt              Python dependencies
├── docker-compose.yml
└── Dockerfile                    FastAPI app container
```
   🧪 Features

    📊 Analytical Endpoints

| Endpoint | Description |
|---------|-------------|
| `GET /api/reports/top-products?limit=10` | Returns most frequently detected products |
| `GET /api/channels/{channel}/activity` | Shows posting activity over time |
| `GET /api/search/messages?query={keyword}` | Searches for messages containing a keyword |

> Visit [http://localhost:8000/docs](http://localhost:8000/docs) to interact with the API.

    🧩 dbt Models

- `stg_telegram_messages`: Cleans and parses raw JSON
- `fct_messages`: Fact table of all messages
- `fct_image_detections`: Detected objects in images
- `dim_channels`: Metadata about each channel
- `dim_dates`: Date spine for time-based analysis


Run dbt models:

```bash
cd src/dbt
dbt --profile telegram_dw run
dbt --profile telegram_dw docs generate
```

Docs available at:  
👉 [http://localhost:8001](http://localhost:8001)

    🚦 Dagster Orchestration

Automate your entire pipeline with Dagster:

     Jobs
- `run_full_pipeline`: Scrape → Load → Transform → Detect

Start the Dagster UI:

```bash
cd src/dagster
dagster dev -f jobs/pipeline_job.py -d ..
```

Visit:  
👉 [http://localhost:3000](http://localhost:3000)

You can:
- Manually launch runs
- Define schedules
- Monitor execution logs per step

   🧰 Installation

    Local Development

```bash
pip install -r requirements.txt
```

    With Docker

```bash
docker-compose up --build
```

   🧪 Example Queries

    Top Products by Detection Count

```sql
SELECT 
    j.value->>'label' AS product,
    COUNT( ) AS count
FROM fct_image_detections fid
CROSS JOIN JSONB_ARRAY_ELEMENTS(fid.detections) AS j
GROUP BY product
ORDER BY count DESC;
```

    Message Activity Over Time

```sql
SELECT 
    DATE_TRUNC('day', message_date) AS day,
    COUNT( ) AS total_messages
FROM fct_messages
GROUP BY day
ORDER BY day DESC;
```

    Search Messages by Keyword

```sql
SELECT message_text, channel, message_date
FROM fct_messages
WHERE message_text ILIKE '%bottle%';
```

   📈 Star Schema Diagram

```
[Fact Tables]
 ├─ fct_messages         ← [Dimensions] dim_channels, dim_dates
 └─ fct_image_detections ← [Dimensions] dim_channels, dim_dates
```

Each fact table links to dimension tables for context and filtering.

   🧑‍💻 Built By
Firaol Delesa
KIAM PROJECTS


