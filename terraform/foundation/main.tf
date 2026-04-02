# main.tf
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~>6.12.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~>6.12.0"
    }
  }

  # # Backend Configuration - hardcode or use partial configuration
  # backend "gcs" {
  #   bucket = "opportune-chess-462012-a3-tf-state"  # Hardcoded, or use -backend-config
  #   prefix = "terraform/state"
  # }
}

provider "google" {
  # credentials = file(var.credentials_file)
  project     = var.project_id
  region      = var.region
}

provider "google-beta" {
  # credentials = file(var.credentials_file)
  project     = var.project_id
  region      = var.region
}

# Enable required APIs first
resource "google_project_service" "required_apis" {
  for_each = toset([
    # "cloudrun.googleapis.com",
    "cloudbuild.googleapis.com",
    "secretmanager.googleapis.com",
    "sql-component.googleapis.com",
    "sqladmin.googleapis.com",
    "artifactregistry.googleapis.com",
    "monitoring.googleapis.com",
    "logging.googleapis.com",
    "dns.googleapis.com",
    "compute.googleapis.com",
    "containerregistry.googleapis.com",
    "vpcaccess.googleapis.com",
    "cloudtrace.googleapis.com",
    "servicenetworking.googleapis.com"
  ])
  
  service                    = each.key
  disable_on_destroy        = false
  disable_dependent_services = false
}

# Add time delay to ensure APIs are ready
resource "time_sleep" "wait_for_apis" {
  depends_on = [google_project_service.required_apis]
  create_duration = "30s"
}

# # Include Networking
# module "networking" {
#   source = "./networking.tf"
# }

# # Include Cloud Run
# module "cloud_run" {
#   source = "./cloud_run.tf"
# }

# # Include Storage
# module "storage" {
#   source = "./storage.tf"
# }

# # Include Database
# module "database" {
#   source = "./database.tf"
# }

# # Include Monitoring
# module "monitoring" {
#   source = "./monitoring.tf"
# }

# # Include Security
# module "security" {
#   source = "./security.tf"
# }

# # Include Logging & Trace
# module "cloud_logging" {
#   source = "./cloud_logging.tf"
# }

# module "cloud_trace" {
#   source = "./cloud_trace.tf"
# }
