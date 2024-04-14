variable "app_name" {
  type        = string
  description = "Application Name"
  default     = "github-data-prep"
}

variable "container_cpu" {
  description = "Container cpu"
  default     = "2000m"
}

variable "container_memory" {
  description = "Container memory"
  default     = "4G"
}

variable "project_id" {
  type        = string
  description = "Github Data Analysis"
  default     = "github-data-analysis-419818"
}

variable "credentials" {
  description = "My Credentials"
  default     = "../../.keys/github-data-analysis.json"
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

variable "repository" {
  type        = string
  description = "The name of the Artifact Registry repository to be created"
  default     = "mage-data-prep"
}



variable "docker_image" {
  type        = string
  description = "The docker image to deploy to Cloud Run."
  default     = "mageai/mageai:latest"
}

variable "domain" {
  description = "Domain name to run the load balancer on. Used if `ssl` is `true`."
  type        = string
  default     = ""
}

variable "ssl" {
  description = "Run load balancer on HTTPS and provision managed certificate with provided `domain`."
  type        = bool
  default     = false
}


variable "service_account_email" {
  description = "service_account_email that are used to run terraform and cloud Run"
  type = string
  default = "github-service@github-data-analysis-419818.iam.gserviceaccount.com"
}


variable "BUCKET_NAME" { 
  description = " "
  type = string
  default = "github-bucket-3615"
}

variable "BUCKET_FOLDER_NAME" { 
  description = " "
  type = string
  default = "raw_github"
}

variable "CHUNK_SIZE" { 
  description = " "
  type = number
  default = 10000
}

variable "Dataset_Id" { 
  description = " "
  type = string
  default = "raw_github_archive"
}

variable "Table_name" { 
  description = " "
  type = string
  default = "april_github_archive"
}

