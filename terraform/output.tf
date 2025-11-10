output "raw_bucket_name" {
  value = google_storage_bucket.raw_bucket.name
}

output "cleaned_bucket_name" {
  value = google_storage_bucket.cleaned_bucket.name
}

output "bigquery_dataset_id" {
  value = google_bigquery_dataset.sales_dataset.dataset_id
}

output "bigquery_table_id" {
  value = google_bigquery_table.sales_table.table_id
}
