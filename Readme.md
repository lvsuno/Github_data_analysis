# Github data processing Pipeline

## Table of contents

- [Project Description](#problem-description)
- [Technologies](#technologies)
- [Data Pipeline Architecture and Workflow](#data-pipeline-architecture-and-workflow)
    - [(1) Ingest historical and (5) moving-forward data to Google Cloud Storage](#1-ingest-historical-and-5-moving-forward-data-to-google-cloud-storage)
    - [(2) BigQuery loads data from Cloud Storage](#2-bigquery-loads-data-from-cloud-storage)
    - [(3) Data Warehouse Transformation with dbt and (6) prefect to schedule incremental transformation](#3-data-warehouse-transformation-with-dbt-and-6-prefect-to-schedule-incremental-transformation)
    - [(4) Data Visualization with Looker](#4-data-visualization-with-looker)
- [Reproducability](#reproducability)
    - [Step 1: Build GCP Resources from Local Computer](#step-1-build-gcp-resources-from-local-computer)
    - [Step 2: Setup Workaround on VM](#step-2-setup-workaround-on-vm)
- [Further Improvements](#further-improvements)



```
terraform -chdir=./infrastructure/gcs+bigquery init

terraform -chdir=./infrastructure/gcs+bigquery  apply
```

```
terraform -chdir=./infrastructure/deploy_mage init

terraform -chdir=./infrastructure/deploy_mage   apply
```