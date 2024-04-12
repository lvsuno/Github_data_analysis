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

terraform -chdir=./infrastructure/deploy_mage apply
```

1. Create a free google cloud account and get your trial of 300$
2.  Grant the following roles to a new service (BigQuery Admin, Cloud SQL Admin, Owner, Storage Admin, Storage Object Admin, Cloud Run Admin, Artifact Registry Reader, Artifact Registry Writer, Serverless VPC Access Admin, Service Account Token Creator, Secret Manager Secret Accessor)
3. Generate an access keys (Json type) and download it
3. Activate BigQuery API, 

### Initial Setup

For this project, we'll use a free version (upto EUR 300 credits). 

1. Create an account with your Google email ID 
2. Setup your  [project](https://console.cloud.google.com/) if you haven't already
    * eg. "Github-data-analysis", and note down the "Project ID" (we'll use this later when deploying infra with TF)
3. Setup [service account & authentication](https://cloud.google.com/docs/authentication/getting-started) for this project
    * Grant `Owner` role.
    * Download service-account-keys (.json) for auth.
4. Download [SDK](https://cloud.google.com/sdk/docs/quickstart) for local setup
5. Set environment variable to point to your downloaded GCP keys:
   ```shell
   export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"

   # gcloud init to set up gcloud
   
   # Refresh token/session, and verify authentication
   gcloud auth application-default login
   ```
   
### Setup for Access
 
1. [IAM Roles](https://cloud.google.com/storage/docs/access-control/iam-roles) for Service account:
   * Go to the *IAM* section of *IAM & Admin* https://console.cloud.google.com/iam-admin/iam
   * Click the *Edit principal* icon for your service account.
   * Add these roles in addition to *Viewer* : **Storage Admin** + **Storage Object Admin** + **BigQuery Admin**
   
2. Enable these APIs for your project:
   * https://console.cloud.google.com/apis/library/iam.googleapis.com
   * https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com
   * https://console.cloud.google.com/apis/api/bigquery.googleapis.com/
   *  For terraform deployment
      * https://console.cloud.google.com/apis/library/artifactregistry.googleapis.com
      * https://console.cloud.google.com/apis/library/cloudresourcemanager.googleapis.com
      * https://console.cloud.google.com/apis/library/vpcaccess.googleapis.com
      * https://console.cloud.google.com/apis/library/secretmanager.googleapis.com
      * https://console.cloud.google.com/apis/library/sqladmin.googleapis.com
      * https://console.cloud.google.com/apis/library/file.googleapis.com
      * https://console.cloud.google.com/apis/library/serviceusage.googleapis.com



https://docs.mage.ai/production/deploying-to-cloud/gcp/setup#secrets