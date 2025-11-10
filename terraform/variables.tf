variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-west4"
}

variable "dataflow_staging_bucket" {
  description = "GCS bucket for Dataflow staging"
  type        = string
  default     = "staging-bucket-temp"
}
