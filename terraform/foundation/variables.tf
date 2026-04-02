variable "project_id" {
  description = "The GCP project ID where resources will be created."
  type        = string
}

variable "tf_state_bucket" {
  description = "bucket to manage state files"
  type = string
}

variable "region" {
  description = "The GCP region where resources will be deployed."
  type        = string
}

variable "domain_name" {
  description = "The domain name for the application."
  type        = string
}

variable "bucket_name" {
  description = "The name of the Cloud Storage bucket for static files."
  type        = string
}

variable "db_user" {
  description = "The username for the Cloud SQL database."
  type        = string
}

variable "db_name" {
  description = "The database name for the Cloud SQL database."
  type        = string
}

variable "db_password" {
  description = "The password for the Cloud SQL database."
  type        = string
  sensitive   = true
}

# ADDED: Missing environment variable
variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "network_name" {
  description = "VPC network name"
  type        = string
}

variable "subnet_name" {
  description = "Subnet name"
  type        = string
}

variable "github_owner" {
  description = "GitHub repository owner"
  type        = string
}

variable "github_repo" {
  description = "GitHub repository name"
  type        = string
}

variable "jwt_secret_key" {
  description = "JWT secret key for authentication"
  type        = string
  sensitive   = true
}

variable "deploy_cloud_run" {
  description = "Whether to deploy Cloud Run service (set to false for initial deployment)"
  type        = bool
  default     = false
}
# # General Project Configuration
# variable "project_id" {
#   description = "The GCP project ID where resources will be created."
#   type        = string
# }

# variable "credentials_file" {
#   description = "Path to the GCP service account credentials file"
# }

# variable "region" {
#   description = "The GCP region where resources will be deployed."
#   type        = string
# }

# variable "tf_state_bucket" {
#   description = "The bucket name for Terraform state storage."
#   type        = string
# }

# # Networking Variables
# variable "domain_name" {
#   description = "The domain name for the application."
#   type        = string
# }

# # Cloud Run Variables
# variable "service_names" {
#   description = "List of Cloud Run service names to be deployed."
#   type        = list(string)
# }

# # Cloud Storage Variables
# variable "bucket_name" {
#   description = "The name of the Cloud Storage bucket for static files."
#   type        = string
# }

# # Cloud SQL Variables
# variable "db_user" {
#   description = "The username for the Cloud SQL database."
#   type        = string
# }

# variable "db_name" {
#   description = "The database for the Cloud SQL database."
#   type        = string
# }
# variable "db_password" {
#   description = "The password for the Cloud SQL database."
#   type        = string
#   sensitive   = true
# }

# # Artifact Registry Variables
# variable "artifact_repo" {
#   description = "The Artifact Registry repository name."
#   type        = string
# }

# # Monitoring Variables
# variable "monitoring_dashboard_path" {
#   description = "Path to the JSON file defining the Cloud Monitoring dashboard."
#   type        = string
#   default     = "dashboards/cloud_run.json"
# }

# # Cloud Logging Variables
# variable "enable_logging" {
#   description = "Enable Cloud Logging for the project."
#   type        = bool
#   default     = true
# }

# # Cloud Trace Variables
# variable "enable_trace" {
#   description = "Enable Cloud Trace for the project."
#   type        = bool
#   default     = true
# }

# # Secret Manager Variables
# variable "secrets" {
#   description = "A map of secrets to be created in Secret Manager."
#   type        = map(string)
#   default     = {
#     "db-connection-url" = "Database connection URL for Cloud SQL"
#   }
# }

# variable "environment" {
#   description = "Environment (dev, staging, prod)"
#   type        = string
# }

# variable "network_name" {
#   description = "VPC network variable"
# }
# variable "subnet_name" {
#   description = "Subnet variable"
#   type = string
# }


# terraform
# ├── foundation
# │   ├── artifact_registry.tf
# │   ├── backend.tf
# │   ├── database.tf
# │   ├── environments
# │   │   ├── common.tfvars
# │   │   ├── dev
# │   │   │   └── config.tfvars
# │   │   ├── prod
# │   │   │   └── config.tfvars
# │   │   └── staging
# │   │       └── config.tfvars
# │   ├── main.tf
# │   ├── networking.tf
# │   ├── output.tf
# │   ├── security.tf
# │   ├── storage.tf
# │   ├── variables.tf
# │   └── workload_identity.tf
# └── service
#     ├── backend.tf
#     ├── cloud_run.tf
#     ├── data.tf
#     ├── environments
#     │   ├── common.tfvars
#     │   ├── dev
#     │   │   └── config.tfvars
#     │   ├── prod
#     │   │   └── config.tfvars
#     │   └── staging
#     │       └── config.tfvars
#     ├── load_balancer.tf
#     ├── main.tf
#     ├── output.tf
#     └── variables.tf


# MediumX
# ├── Dockerfile
# ├── README.md
# ├── Upload
# │   └── images
# │       ├── 1731914484459355.jpg
# │       ├── 1731914853421845.jpg
# │       ├── 1731944894405957.jpg
# ├── alembic
# │   ├── README
# │   ├── env.py
# │   ├── script.py.mako
# │   └── versions
# │       ├── 53c00c837b7d_adding_image_post_column_in_posts_table.py
# │       └── edc24056085e_initial_migration_blogging_db_tables.py
# ├── alembic.ini
# ├── app
# │   ├── Upload
# │   │   └── images
# │   ├── __init__.py
# │   ├── core
# │   │   ├── __init__.py
# │   │   ├── config.py
# │   │   └── database.py
# │   ├── main.py
# │   ├── models
# │   │   ├── __init__.py
# │   │   ├── commentModel.py
# │   │   ├── likeModel.py
# │   │   ├── postModel.py
# │   │   └── userModel.py
# │   ├── modelsOperaions
# │   │   ├── comment.py
# │   │   ├── like.py
# │   │   ├── post.py
# │   │   └── user.py
# │   ├── oauth2.py
# │   ├── routers
# │   │   ├── auth.py
# │   │   ├── comment.py
# │   │   ├── like.py
# │   │   ├── post.py
# │   │   └── user.py
# │   ├── schemas
# │   │   ├── commentsSchemas.py
# │   │   ├── likeSchemas.py
# │   │   ├── postSchemas.py
# │   │   └── userSchemas.py
# │   ├── services
# │   │   └── storage.py
# │   └── utils.py
# ├── client
# │   ├── Dockerfile
# │   ├── blog.html
# │   ├── css
# │   │   ├── blogpost.css
# │   │   ├── mobile.css
# │   │   ├── signInSignUp.css
# │   │   ├── style.css
# │   │   ├── utils.css
# │   │   └── write.css
# │   ├── img
# │   │   ├── Medium_(website)-Logo.wine.png
# │   │   ├── Medium_(website)-Logo1.wine.png
# │   │   ├── X.png
# │   │   ├── logo.png
# │   │   ├── logo1.png
# │   │   ├── logo2.png
# │   │   ├── medium-homepage.webp   
# │   ├── index.html
# │   ├── js
# │   │   ├── blog.js
# │   │   ├── config.js
# │   │   ├── script.js
# │   │   ├── search.js
# │   │   ├── signInSignUp.js
# │   │   └── write.js
# │   ├── nginx.conf
# │   ├── search.html
# │   ├── svg
# │   │   ├── addImg.svg
# │   │   ├── bold.svg
# │   │   ├── comment.svg
# │   │   ├── itelic.svg
# │   │   ├── like.svg
# │   └── write.html
# ├── cloud-sql-key.json
# ├── docker-compose-dev.yml
# ├── docker-compose-prod.yml
# ├── nginx
# │   └── nginx.conf
# ├── pytest.ini
# ├── terraform
# │   ├── foundation
# │   │   ├── artifact_registry.tf
# │   │   ├── backend.tf
# │   │   ├── database.tf
# │   │   ├── environments
# │   │   │   ├── common.tfvars
# │   │   │   ├── dev
# │   │   │   │   └── config.tfvars
# │   │   │   ├── prod
# │   │   │   │   └── config.tfvars
# │   │   │   └── staging
# │   │   │       └── config.tfvars
# │   │   ├── main.tf
# │   │   ├── networking.tf
# │   │   ├── output.tf
# │   │   ├── security.tf
# │   │   ├── storage.tf
# │   │   ├── variables.tf
# │   │   └── workload_identity.tf
# │   └── service
# │       ├── backend.tf
# │       ├── cloud_run.tf
# │       ├── data.tf
# │       ├── environments
# │       │   ├── common.tfvars
# │       │   ├── dev
# │       │   │   └── config.tfvars
# │       │   ├── prod
# │       │   │   └── config.tfvars
# │       │   └── staging
# │       │       └── config.tfvars
# │       ├── load_balancer.tf
# │       ├── main.tf
# │       ├── output.tf
# │       └── variables.tf
# └── tests
#     ├── __init__.py
#     ├── conftest.py
#     ├── test_posts.py
#     └── test_users.py