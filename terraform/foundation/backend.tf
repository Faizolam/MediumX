# Backend Configuration
terraform {
  backend "gcs" {
    bucket = "mediumx-dev-tf-state"
    prefix = "foundation/state"
  }
}



# gcloud storage buckets add-iam-policy-binding "gs://mediumx-dev-tf-state/" \
#   --member="serviceAccount:mediumx-service-account@mediumx-483502.iam.gserviceaccount.com" \
#   --role="roles/storage.objectAdmin"

# gcloud storage buckets add-iam-policy-binding "gs://mediumx-dev-tf-state/" \
#   --member="serviceAccount:mediumx-service-account@mediumx-483502.iam.gserviceaccount.com" \
#   --role="roles/storage.objectViewer"

# gcloud storage ls gs://mediumx-dev-tf-state/ --account=mediumx-service-account@mediumx-483502.iam.gserviceaccount.com


# gcloud storage buckets add-iam-policy-binding "gs://mediumx-dev-tf-state" \
#   --member="serviceAccount:mediumx-service-account@mediumx-483502.iam.gserviceaccount.com" \
#   --role="roles/storage.objectAdmin"

# gcloud storage ls gs://mediumx-dev-tf-state/ \
#   --account=mediumx-service-account@mediumx-483502.iam.gserviceaccount.com