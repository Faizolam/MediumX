# ===== outputs.tf (New file) =====
output "workload_identity_provider" {
  description = "The full name of the Workload Identity Provider for GitHub Actions"
  value       = google_iam_workload_identity_pool_provider.github_provider.name
}

output "github_actions_service_account" {
  description = "The email of the GitHub Actions service account"
  value       = google_service_account.github_actions_sa.email
}

# ADDED: Missing cloud_run_sa output
output "cloud_run_sa" {
  description = "Cloud Run service account details"
  value = {
    email = google_service_account.cloud_run_sa.email
    id    = google_service_account.cloud_run_sa.id
  }
}

output "static_bucket_url" {
  description = "Public URL for static files bucket"
  value       = "https://storage.googleapis.com/${google_storage_bucket.static_files.name}"
}

output "uploads_bucket_url" {
  description = "Public URL for user uploads bucket"
  value       = "https://storage.googleapis.com/${google_storage_bucket.user_uploads.name}"
}

# CORRECTED: Consistent naming
output "static_bucket_name" {
  description = "Name of the static files bucket"
  value       = google_storage_bucket.static_files.name
}

output "uploads_bucket_name" {
  description = "Name of the user uploads bucket"
  value       = google_storage_bucket.user_uploads.name
}

output "project_id" {
  description = "The GCP project ID"
  value       = var.project_id
}

output "region" {
  description = "The GCP region"
  value       = var.region
}

output "artifact_registry_repository" {
  description = "The Artifact Registry repository name"
  value       = google_artifact_registry_repository.backend_repo.repository_id
}

output "database_connection_name" {
  description = "The Cloud SQL connection name"
  value       = google_sql_database_instance.mediumx_db_instance.connection_name
}

output "database_user" {
  description = "The database user"
  value       = google_sql_user.user.name
}

output "database_name" {
  description = "The database name"
  value       = google_sql_database.database.name
}

output "vpc_connector_id" {
  description = "VPC connector ID"
  value = google_vpc_access_connector.connector.id
}
output "vpc_connector_name" {
  description = "VPC connector Name"
  value = google_vpc_access_connector.connector.name
}

# ADDED: Secret outputs
output "db_password_secret_name" {
  description = "Database password secret name"
  value       = google_secret_manager_secret.db_password_secret.secret_id
}

output "jwt_secret_name" {
  description = "JWT secret name"
  value       = google_secret_manager_secret.jwt_secret.secret_id
}

# ADD to existing outputs.tf
output "static_ip_address" {
  description = "Static IP address for load balancer"
  value       = google_compute_global_address.static_ip.address
}

output "static_ip_name" {
  description = "Static IP resource name"
  value       = google_compute_global_address.static_ip.name
}