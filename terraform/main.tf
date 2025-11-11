# -----------------------------
# Storage Buckets
# -----------------------------

# Raw Data Bucket
resource "google_storage_bucket" "raw_bucket" {
  name          = "${var.project_id}-raw-buckettt"
  location      = var.region
  storage_class = "STANDARD"
  force_destroy = true
}

# Cleaned Data Bucket
resource "google_storage_bucket" "cleaned_bucket" {
  name          = "${var.project_id}-cleaned-buckettt"
  location      = var.region
  storage_class = "STANDARD"
  force_destroy = true
}

# Upload raw CSV file to the raw bucket
resource "google_storage_bucket_object" "raw_data" {
  name   = "custom_sales_dataset.csv"
  bucket = google_storage_bucket.raw_bucket.name
  source = "${path.module}/../data/custom_sales_dataset.csv"
}

# -----------------------------
# BigQuery Dataset & Table
# -----------------------------

# Dataset for cleaned sales data
resource "google_bigquery_dataset" "sales_dataset" {
  dataset_id                 = "cleaned_sales_data"
  location                   = var.region
  delete_contents_on_destroy = true
}

# BigQuery table definition
resource "google_bigquery_table" "sales_table" {
  dataset_id          = google_bigquery_dataset.sales_dataset.dataset_id
  table_id            = "sales_cleaned"
  deletion_protection = false
  schema              = file("${path.module}/schema.json")
}
