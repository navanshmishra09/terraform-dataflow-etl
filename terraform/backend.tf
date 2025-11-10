terraform {
  required_version = ">= 1.0"

  backend "gcs" {
    bucket = "state-buckettt" # Replace with your GCS bucket for state
    prefix = "terraform/state"
  }
}
