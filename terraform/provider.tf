terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.0.0"
    }
  }
}

provider "google" {
  project = "devops-training-475116" # <-- replace with your actual GCP project ID
  region  = "us-west4"
}
