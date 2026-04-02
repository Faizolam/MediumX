# security.tf 
resource "google_secret_manager_secret" "db_password_secret" {
  secret_id = "db-password-secret"
  
  replication {
    auto {}
  }
  
  depends_on = [time_sleep.wait_for_apis]
}

resource "google_secret_manager_secret_version" "db_password_secret_version" {
  secret      = google_secret_manager_secret.db_password_secret.id
  secret_data = var.db_password
}

resource "google_secret_manager_secret" "jwt_secret" {
  secret_id = "jwt-secret-key"
  
  replication {
    auto {}
  }
  
  depends_on = [time_sleep.wait_for_apis]
}

resource "google_secret_manager_secret_version" "jwt_secret_version" {
  secret      = google_secret_manager_secret.jwt_secret.id
  secret_data = var.jwt_secret_key
}

resource "google_service_account" "cloud_run_sa" {
  account_id   = "mediumx-cloud-run-sa"
  display_name = "MediumX Cloud Run Service Account"
}

# Grant Cloud Run service account access to secrets
resource "google_secret_manager_secret_iam_member" "db_password_access" {
  secret_id = google_secret_manager_secret.db_password_secret.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "jwt_secret_access" {
  secret_id = google_secret_manager_secret.jwt_secret.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

# =====================================================================================



# resource "google_project_service" "secretmanager" {
#   service = "secretmanager.googleapis.com"
# }


# resource "google_secret_manager_secret" "db_user_secret" {
#   secret_id = var.db_user

#   replication {
#     auto {}
#   }
#   depends_on = [ google_project_service.secretmanager ]
# }

# resource "google_secret_manager_secret_version" "db_user_secret_version" {
#   secret      = google_secret_manager_secret.db_user_secret.id
#   secret_data = var.db_user
# }


# resource "google_secret_manager_secret" "db_pass_secret" {
#   secret_id = var.db_password
#   replication {
#     auto {}
#   }
#   depends_on = [ google_project_service.secretmanager ]
# }

# resource "google_secret_manager_secret_version" "db_pass_secret_version" {
#   secret      = google_secret_manager_secret.db_pass_secret.id
#   secret_data = var.db_password
# }