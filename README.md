# Retail Data Transformation Pipeline

This repository contains an Apache Airflow DAG that orchestrates a robust data pipeline for transforming and analyzing online retail data. The pipeline leverages Google Cloud Platform (GCP) services (Google Cloud Storage, BigQuery), dbt for data transformations, and Soda for continuous data quality checks.

## Project Overview

The goal of this project is to ingest raw online retail transaction data, apply various transformations, ensure data quality at each critical stage, and prepare it for reporting and analysis in a data warehouse (Google BigQuery).

### Key Technologies Used

* **Apache Airflow**: For orchestrating and scheduling the data pipeline.
* **Google Cloud Platform (GCP)**:
    * **Google Cloud Storage (GCS)**: For raw data staging.
    * **Google BigQuery**: As the data warehouse for transformed and reported data.
* **dbt (data build tool)**: For defining, transforming, and modeling data within BigQuery.
* **Soda Core**: For implementing comprehensive data quality checks throughout the pipeline.
* **Astro SDK (formerly Astro SDK for Apache Airflow)**: Simplifies data loading and interaction with data systems.
* **Cosmos (dbt + Airflow)**: Enables seamless integration of dbt projects directly within Airflow DAGs.

### Pipeline Stages

The `retail` DAG orchestrates the following sequence of operations:

1.  **`upload_csv_gcp`**: Transfers the raw `online_retail.txt` (CSV) file from the local Airflow `include/dataset` directory to a specified GCS bucket (`ahmedmarzouk-online-retail`).
2.  **`create_retail_dataset`**: Creates an empty BigQuery dataset named `retail` to house our transformed data.
3.  **`gcs_to_raw`**: Uses Astro SDK to load the raw `online_retail.csv` from GCS into a BigQuery table named `raw_invoices` within the `retail` dataset.
4.  **`check_load`**: (Soda Data Quality Check) Executes data quality checks on the newly loaded `raw_invoices` table, focusing on `sources` related checks.
5.  **`transform`**: (dbt Task Group) Executes dbt models located in the `models/transform` directory. These models cleanse, denormalize, and enrich the raw data.
6.  **`check_transform`**: (Soda Data Quality Check) Runs data quality checks on the output of the `transform` stage, ensuring the transformed data meets quality standards.
7.  **`report`**: (dbt Task Group) Executes dbt models located in the `models/report` directory. These models aggregate and prepare data for final reporting purposes.
8.  **`check_report`**: (Soda Data Quality Check) Performs final data quality checks on the reporting tables before they are consumed by downstream tools like Metabase.

### Directory Structure

Okay, this looks like a well-structured and comprehensive data pipeline! I can definitely generate a README for GitHub and a LinkedIn post based on this Airflow DAG.

GitHub README.md
Markdown

# Retail Data Transformation Pipeline

This repository contains an Apache Airflow DAG that orchestrates a robust data pipeline for transforming and analyzing online retail data. The pipeline leverages Google Cloud Platform (GCP) services (Google Cloud Storage, BigQuery), dbt for data transformations, and Soda for continuous data quality checks.

## Project Overview

The goal of this project is to ingest raw online retail transaction data, apply various transformations, ensure data quality at each critical stage, and prepare it for reporting and analysis in a data warehouse (Google BigQuery).

### Key Technologies Used

* **Apache Airflow**: For orchestrating and scheduling the data pipeline.
* **Google Cloud Platform (GCP)**:
    * **Google Cloud Storage (GCS)**: For raw data staging.
    * **Google BigQuery**: As the data warehouse for transformed and reported data.
* **dbt (data build tool)**: For defining, transforming, and modeling data within BigQuery.
* **Soda Core**: For implementing comprehensive data quality checks throughout the pipeline.
* **Astro SDK (formerly Astro SDK for Apache Airflow)**: Simplifies data loading and interaction with data systems.
* **Cosmos (dbt + Airflow)**: Enables seamless integration of dbt projects directly within Airflow DAGs.

### Pipeline Stages

The `retail` DAG orchestrates the following sequence of operations:

1.  **`upload_csv_gcp`**: Transfers the raw `online_retail.txt` (CSV) file from the local Airflow `include/dataset` directory to a specified GCS bucket (`ahmedmarzouk-online-retail`).
2.  **`create_retail_dataset`**: Creates an empty BigQuery dataset named `retail` to house our transformed data.
3.  **`gcs_to_raw`**: Uses Astro SDK to load the raw `online_retail.csv` from GCS into a BigQuery table named `raw_invoices` within the `retail` dataset.
4.  **`check_load`**: (Soda Data Quality Check) Executes data quality checks on the newly loaded `raw_invoices` table, focusing on `sources` related checks.
5.  **`transform`**: (dbt Task Group) Executes dbt models located in the `models/transform` directory. These models cleanse, denormalize, and enrich the raw data.
6.  **`check_transform`**: (Soda Data Quality Check) Runs data quality checks on the output of the `transform` stage, ensuring the transformed data meets quality standards.
7.  **`report`**: (dbt Task Group) Executes dbt models located in the `models/report` directory. These models aggregate and prepare data for final reporting purposes.
8.  **`check_report`**: (Soda Data Quality Check) Performs final data quality checks on the reporting tables before they are consumed by downstream tools like Metabase.

### Directory Structure

.
├── dags/
│   └── retail.py                 # The main Airflow DAG file
├── include/
│   ├── dataset/
│   │   └── online_retail.txt     # Raw input data file
│   ├── dbt/
│   │   ├── dbt_project.yml       # dbt project configuration
│   │   ├── packages.yml          # dbt package dependencies
│   │   ├── profiles.yml          # dbt connection profiles
│   │   ├── models/
│   │   │   ├── transform/        # dbt models for data transformation
│   │   │   └── report/           # dbt models for reporting layer
│   │   └── cosmos_config.py      # Cosmos dbt integration configuration
│   └── soda/
│       └── check_function.py     # Python function to execute Soda scans
│       └── checks/               # Soda checks definitions (e.g., sources.yml, transform.yml, report.yml)
├── Dockerfile                    # Dockerfile for building the Astro project image
└── packages.txt                  # Python dependencies for the Airflow environment


## Setup and Deployment

This project is designed to be deployed using Astro CLI.

1.  **Prerequisites**:
    * Docker Desktop installed and running.
    * Astro CLI installed.
    * A GCP Project with billing enabled.
    * A GCP Service Account Key (JSON) with permissions for GCS, BigQuery, and BigQuery Dataset Editor roles. Save this key (e.g., `service_account.json`) in your project's `gcp/` directory.
    * Ensure your `gcp` connection is set up in Airflow (or via environment variables for `astro dev start`).

2.  **Project Initialization (if new)**:
    ```bash
    # If you haven't already, create a new Astro project
    astro dev init
    ```

3.  **Add GCP Connection**:
    Ensure your `airflow_settings.yaml` (or equivalent Airflow UI connection) has a `gcp` connection configured with your service account key.

4.  **Install dbt and Soda Dependencies**:
    Make sure your `Dockerfile` includes the necessary steps to install `dbt-bigquery`, `soda-core-bigquery`, and other Python dependencies in your `dbt_venv` and `soda_venv` virtual environments.
    *A critical step involves ensuring correct permissions for dbt package installation. Refer to the `Dockerfile` for `chown` and `rm -rf` commands before `dbt deps`.*

5.  **Local Development**:
    To start the Airflow environment locally:
    ```bash
    astro dev start
    ```
    This will build the Docker image (including running `dbt deps` and installing Soda dependencies) and start the Airflow services.

6.  **Access Airflow UI**:
    Once started, access the Airflow UI typically at `http://localhost:8080`. You should see the `retail` DAG ready to be triggered.

## Running the Pipeline

Once the Astro environment is up:

1.  **Ensure `online_retail.txt` is in `include/dataset/`**.
2.  **Trigger the `retail` DAG** from the Airflow UI.
3.  Monitor the task progress and observe the data being processed in GCS and BigQuery.

## Data Quality Checks

Soda checks are integrated at multiple points in the pipeline to ensure data integrity and reliability.
* `check_load` verifies the raw data after ingestion.
* `check_transform` validates the data after the initial dbt transformations.
* `check_report` confirms the quality of the final reporting tables.

The configurations for these checks are located in the `include/soda/checks/` directory.
