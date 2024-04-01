variable "project_id" {
  type        = string
  description = "Github Data Analysis"
  default     = "github-data-analysis-418315"
}

variable "credentials" {
  description = "My Credentials"
  default     = "../../.keys/github-data-analysis-418315-96023170ca9a.json"
}

variable "region" {
  type        = string
  description = "The default compute region"
  default     = "us-central1"
}

variable "zone" {
  type        = string
  description = "The default compute zone"
  default     = "us-central1-c"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default     = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  #Update the below to what you want your dataset to be called
  default     = "raw_github_archive"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  #Update the below to a unique bucket name
  default     = "github-bucket-3615"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}