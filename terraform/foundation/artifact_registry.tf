# ===== artifact_registry.tf =====
resource "google_artifact_registry_repository" "backend_repo" {
  location      = var.region
  repository_id = "mediumx-backend-repo"
  description   = "Repository for MediumX backend Docker images"
  format        = "DOCKER"
  
  depends_on = [time_sleep.wait_for_apis]
}