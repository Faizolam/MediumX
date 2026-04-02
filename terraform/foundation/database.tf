# database.tf 
resource "google_sql_database_instance" "mediumx_db_instance" {
  name                = "${var.environment}-mediumx-db-instance"
  database_version    = "POSTGRES_15"
  region              = var.region
  deletion_protection = false

  settings {
    tier = "db-f1-micro"
    
    ip_configuration {
      ipv4_enabled    = true
      private_network = google_compute_network.vpc_network.id
    }
    
    backup_configuration {
      enabled = false  # Enable in production
    }
  }

  depends_on = [
    google_service_networking_connection.private_vpc_connection,
    time_sleep.wait_for_apis
  ]
}

resource "google_sql_database" "database" {
  name     = var.db_name
  instance = google_sql_database_instance.mediumx_db_instance.name
}

resource "google_sql_user" "user" {
  name     = var.db_user
  instance = google_sql_database_instance.mediumx_db_instance.name
  password = var.db_password
}



# resource "google_sql_database_instance" "mediumx_db_instance" {
#   name             = "mediumx-db-instance"
#   database_version = "POSTGRES_15"
#   region           = var.region
#   deletion_protection = false
#   settings {
#     tier = "db-f1-micro"
#   }
# }

# resource "google_sql_database" "database" {
#   name     = "mediumx"
#   instance = google_sql_database_instance.mediumx_db_instance.name
# }

# resource "google_sql_user" "user" {
#   name     = var.db_user
#   instance = google_sql_database_instance.mediumx_db_instance.name
#   password = var.db_password
# }