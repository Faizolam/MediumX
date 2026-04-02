# Add these to your Terraform configuration
# Remove the Cloud Build trigger from previous suggestions since we're using GitHub Actions

# =====(Add Workload Identity Federation)=====

# Create Workload Identity Pool for GitHub Actions
resource "google_iam_workload_identity_pool" "github_pool" {
  workload_identity_pool_id = "github-actions-${random_id.pool_suffix.hex}"
  display_name              = "GitHub Actions Pool"
  description               = "Identity pool for GitHub Actions workflows"
  depends_on                = [time_sleep.wait_for_apis]
}

# Instead of fighting GCP soft-delete:
resource "random_id" "pool_suffix" {
  byte_length = 4
}

# Create Workload Identity Provider for GitHub
resource "google_iam_workload_identity_pool_provider" "github_provider" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github_pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider"
  display_name                       = "GitHub Provider"
  description                        = "OIDC identity pool provider for GitHub Actions"

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
    "attribute.ref"        = "assertion.ref"
  }

  oidc {
    issuer_uri        = "https://token.actions.githubusercontent.com"
    allowed_audiences = []
  }

  attribute_condition = "assertion.repository=='${var.github_owner}/${var.github_repo}'"
}

# Service Account for GitHub Actions
resource "google_service_account" "github_actions_sa" {
  account_id   = "github-actions-sa"
  display_name = "GitHub Actions Service Account"
  description  = "Service account used by GitHub Actions for deployment"
}

# Allow GitHub Actions to impersonate the service account
resource "google_service_account_iam_binding" "github_actions_workload_identity" {
  service_account_id = google_service_account.github_actions_sa.name
  role               = "roles/iam.workloadIdentityUser"

  members = [
    "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github_pool.name}/attribute.repository/${var.github_owner}/${var.github_repo}"
  ]
}

# Grant necessary permissions to GitHub Actions service account
resource "google_project_iam_member" "github_actions_permissions" {
  for_each = toset([
    "roles/run.admin",                    # Deploy to Cloud Run
    "roles/storage.admin",                # Upload frontend files
    "roles/artifactregistry.writer",     # Push Docker images
    "roles/cloudsql.client",             # Run migrations
    "roles/secretmanager.secretAccessor", # Access secrets for migrations
    "roles/iam.serviceAccountUser"        # Use Cloud Run service account
  ])
  
  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.github_actions_sa.email}"
}