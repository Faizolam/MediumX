# =============================================================================
# CLOUD STORAGE CONFIGURATION
# =============================================================================
# This file contains all Cloud Storage bucket configurations for the MediumX
# application, including static file hosting and user upload management.
# =============================================================================

# =============================================================================
# STATIC FILES BUCKET
# =============================================================================
# Primary bucket for hosting frontend static assets
# Serves HTML, CSS, JavaScript, images, and other static content

resource "google_storage_bucket" "static_files" {
  name     = "${var.project_id}-${var.bucket_name}"
  location = var.region
  project  = var.project_id

  # Security and access configuration
  uniform_bucket_level_access = true  # Use IAM instead of ACLs
  force_destroy               = true  # Allow destruction in dev environment

  # Website hosting configuration
  website {
    main_page_suffix = "index.html"  # Default page for directory requests
    not_found_page   = "404.html"    # Custom 404 error page
  }

  # CORS configuration for cross-origin requests from frontend
  cors {
    origin = [
      "https://${var.domain_name}",  # Production domain
      "http://localhost:3000"        # Local development
    ]
    method          = ["GET", "HEAD", "PUT", "POST", "DELETE"]
    response_header = ["*"]
    max_age_seconds = 3600  # Cache CORS preflight for 1 hour
  }

  # Versioning disabled for static files (not needed)
  versioning {
    enabled = false
  }
  
  depends_on = [time_sleep.wait_for_apis]
}

# =============================================================================
# USER UPLOADS BUCKET
# =============================================================================
# Secure bucket for user-generated content (profile images, article images, etc.)

resource "google_storage_bucket" "user_uploads" {
  name     = "${var.project_id}-mediumx-uploads"
  location = var.region
  project  = var.project_id

  # Security configuration
  uniform_bucket_level_access = true
  force_destroy               = false  # Protect user data in all environments

  # CORS configuration for file uploads from frontend
  cors {
    origin = [
      "https://${var.domain_name}",  # Production domain
      "http://localhost:3000"        # Local development
    ]
    method          = ["GET", "HEAD", "PUT", "POST", "DELETE"]
    response_header = ["*"]
    max_age_seconds = 3600
  }

  # Lifecycle management for cost optimization
  lifecycle_rule {
    condition {
      age = 365  # Files older than 1 year
    }
    action {
      type = "Delete"  # Automatically delete old files
    }
  }

  # Additional lifecycle rule for incomplete multipart uploads
  lifecycle_rule {
    condition {
      age                   = 7  # Clean up after 7 days
      matches_storage_class = []
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }

  # Versioning configuration for user content protection
  versioning {
    enabled = false  # Disable to save storage costs
  }
  
  depends_on = [time_sleep.wait_for_apis]
}

# =============================================================================
# BUCKET IAM PERMISSIONS
# =============================================================================
# Configure access permissions for public content serving

# Allow public read access to static files (website content)
resource "google_storage_bucket_iam_member" "static_public_read" {
  bucket = google_storage_bucket.static_files.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

# Allow public read access to user uploads (profile images, article images)
resource "google_storage_bucket_iam_member" "uploads_public_read" {
  bucket = google_storage_bucket.user_uploads.name
  role   = "roles/storage.objectViewer"
  member = "allUsers"
}

# =============================================================================
# CLOUD RUN STORAGE PERMISSIONS
# =============================================================================
# Grant Cloud Run service account appropriate access to storage buckets

# Full access to user uploads bucket for file management
resource "google_storage_bucket_iam_member" "cloud_run_uploads_admin" {
  bucket = google_storage_bucket.user_uploads.name
  role   = "roles/storage.objectAdmin"  # Create, read, update, delete objects
  member = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

# Read access to static files bucket (if needed for serving)
resource "google_storage_bucket_iam_member" "cloud_run_static_read" {
  bucket = google_storage_bucket.static_files.name
  role   = "roles/storage.objectViewer"  # Read-only access
  member = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

# =============================================================================
# GITHUB ACTIONS STORAGE PERMISSIONS
# =============================================================================
# Grant GitHub Actions service account deployment permissions

# Full admin access to static files bucket for frontend deployment
resource "google_storage_bucket_iam_member" "github_static_admin" {
  bucket = google_storage_bucket.static_files.name
  role   = "roles/storage.admin"  # Full bucket management for deployment
  member = "serviceAccount:${google_service_account.github_actions_sa.email}"
}

# Limited access to uploads bucket (for potential cleanup tasks)
resource "google_storage_bucket_iam_member" "github_uploads_read" {
  bucket = google_storage_bucket.user_uploads.name
  role   = "roles/storage.objectViewer"  # Read-only access
  member = "serviceAccount:${google_service_account.github_actions_sa.email}"
}

# =============================================================================
# STORAGE BUCKET NOTIFICATIONS (Optional)
# =============================================================================
# Uncomment if you need to trigger functions on file uploads

# resource "google_storage_notification" "upload_notification" {
#   bucket         = google_storage_bucket.user_uploads.name
#   payload_format = "JSON_API_V1"
#   topic          = google_pubsub_topic.upload_topic.id  # Define topic separately
#   event_types = [
#     "OBJECT_FINALIZE",  # File upload completed
#     "OBJECT_DELETE"     # File deleted
#   ]
#   
#   custom_attributes = {
#     environment = var.environment
#   }
# }




















# ===============================================================================================================
# # 5. Frontend deployment to Cloud Storage
# resource "google_storage_bucket_object" "frontend_files" {
#   for_each = fileset("${path.module}/../client", "**/*")
  
#   bucket = google_storage_bucket.static_files.name
#   name   = each.value
#   source = "${path.module}/../client/${each.value}"
  
#   # Set content type based on file extension
#   content_type = lookup({
#     "html" = "text/html",
#     "css"  = "text/css",
#     "js"   = "application/javascript",
#     "png"  = "image/png",
#     "jpg"  = "image/jpeg",
#     "jpeg" = "image/jpeg",
#     "svg"  = "image/svg+xml"
#   }, split(".", each.value)[length(split(".", each.value)) - 1], "application/octet-stream")
  
#   depends_on = [google_storage_bucket.static_files]
# }




# # ===== storage.tf (Add user uploads bucket) =====
# resource "google_storage_bucket" "user_uploads" {
#   name     = "${var.project_id}-mediumx-uploads"
#   location = var.region
#   project  = var.project_id

#   uniform_bucket_level_access = true
#   force_destroy               = false  # Protect user data in production

#   cors {
#     origin          = ["https://${var.domain_name}", "http://localhost:3000"]
#     method          = ["GET", "HEAD", "PUT", "POST", "DELETE"]
#     response_header = ["*"]
#     max_age_seconds = 3600
#   }

#   lifecycle_rule {
#     condition {
#       age = 365  # Delete files older than 1 year
#     }
#     action {
#       type = "Delete"
#     }
#   }
  
#   depends_on = [time_sleep.wait_for_apis]
# }

# # Make user uploads publicly readable
# resource "google_storage_bucket_iam_member" "user_uploads_public_read" {
#   bucket = google_storage_bucket.user_uploads.name
#   role   = "roles/storage.objectViewer"
#   member = "allUsers"
# }


# resource "google_storage_bucket" "static_files" {
#   name     = var.bucket_name
#   location = var.region
#   project  = var.project_id

#   uniform_bucket_level_access = true

#   website {
#     main_page_suffix = "index.html"
#     not_found_page   = "404.html"
#   }

#   cors {
#     origin          = ["${var.domain_name}"]
#     method          = ["GET", "HEAD", "PUT", "POST", "DELETE"]
#     response_header = ["*"]
#     max_age_seconds = 3600
#   }
# }
