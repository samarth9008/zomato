# Zomato Batch Pipeline

A daily food-delivery analytics pipeline using Airflow, Snowflake, and dbt.

## Data flow

```text
S3 CSV files → Snowflake RAW tables → dbt staging views → analytics marts
```

Airflow loads the raw files and runs the dbt models each day.

Link to the raw files - https://drive.google.com/drive/folders/1_dwsOGOMeiklN4Xi6_wAJoQ7-OuKLnQM

## Project structure

- `airflow/` — Docker setup and the batch DAG
- `snowflake/` — warehouse, S3 integration, stage, and raw-table SQL
- `zomato_dbt/` — staging, dimension, fact, and reporting models
- `aws/` — Snowflake storage-integration trust-policy template

## Snowflake storage integration

`ZOMATO_S3_INT` lets Snowflake access the S3 bucket through an AWS IAM role, without storing AWS access keys in Snowflake.

1. Create an IAM role with access to the bucket.
2. Add its ARN and the bucket name to `snowflake/02_storage_integration.sql`, then run the script.
3. Run `DESC INTEGRATION ZOMATO_S3_INT` and copy the returned IAM user ARN and external ID into `aws/snowflake_role.json` before applying it as the role's trust policy.
4. Run `snowflake/03_stage_and_format.sql` to create the external stage.

See [Configure a Snowflake storage integration for Amazon S3](https://docs.snowflake.com/en/user-guide/data-load-s3-config-storage-integration) for the complete AWS setup.

## Run locally

1. Execute the scripts in `snowflake/` in numeric order and replace the S3 placeholders.
2. Copy `airflow/.env.example` to `airflow/.env` and add your Snowflake credentials.
3. Start Airflow:

```bash
cd airflow
docker compose up --build -d
```

Open <http://localhost:8080> and run the `zomato_batch` DAG.
