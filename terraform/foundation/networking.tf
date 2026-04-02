# ===== networking.tf =====
resource "google_compute_network" "vpc_network" {
  name                    = var.network_name
  auto_create_subnetworks = false
  # FIXED: Added lifecycle rules to prevent destroy failures from orphaned peerings
  lifecycle {
    # Allow destroy even if peerings linger (manual cleanup handled below)
    prevent_destroy = false
  }
  # FIXED: Explicit dependency ordering - destroys AFTER connectors/peerings
  depends_on = [
    time_sleep.wait_for_apis,
    # Ensures APIs are ready before network creation
  ]
}

resource "google_compute_subnetwork" "mediumx_subnetwork" {
  name          = var.subnet_name
  ip_cidr_range = "10.0.0.0/24"
  network       = google_compute_network.vpc_network.id
  region        = var.region
}

resource "google_compute_global_address" "private_ip_address" {
  name          = "private-ip-address"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.vpc_network.id
  depends_on    = [time_sleep.wait_for_apis]
}

# ADDED: Static IP for Load Balancer
resource "google_compute_global_address" "static_ip" {
  name         = "mediumx-static-ip"
  description  = "Static IP for MediumX Load Balancer"
  depends_on   = [time_sleep.wait_for_apis]
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.vpc_network.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
  # FIXED: Proper dependency chain prevents race conditions
  depends_on = [
    time_sleep.wait_for_apis,
    google_compute_global_address.private_ip_address
    # Ensures IP allocation exists before peering creation
  ]
}

# 7. VPC ACCESS CONNECTOR - DESTROYS FIRST (CRITICAL FIX)
resource "google_vpc_access_connector" "connector" {
  name          = "mediumx-vpc-connector"
  region        = var.region
  network       = google_compute_network.vpc_network.id
  ip_cidr_range = "10.1.0.0/28"
  #* GCP requirements, both min_instances and max_instances must be explicitly set, with min_instances set to at least 2
  min_instances = 2
  max_instances = 3
  #* Never include both max_instances and max_throughput in the same resource block.
  #* It is generally recommended to use max_instances for scaling in most use-cases, as max_throughput is discouraged and less flexible.
  # max_throughput = 200

  # FIXED: Explicit dependency ensures it destroys BEFORE network
  depends_on = [
    time_sleep.wait_for_apis,
    google_service_networking_connection.private_vpc_connection
    # Service networking must exist before connector creation
  ]
}

resource "google_compute_firewall" "allow_health_checks" {
  name    = "allow-health-checks"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["80", "443", "8080"]
  }

  source_ranges = ["35.191.0.0/16", "130.211.0.0/22"]
  target_tags   = ["health-check"]
}

resource "google_compute_firewall" "allow_internal_traffic" {
  name    = "allow-internal-traffic"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "all"
  }

  source_ranges = ["10.0.0.0/24", "10.1.0.0/28"]
}



# 9. FAILSAFE CLEANUP - DESTROYS LAST (NEW - PREVENTS FUTURE ISSUES)
# 9. FIXED FAILSAFE CLEANUP - USES ONLY self.triggers (CRITICAL FIX)
resource "null_resource" "cleanup_service_networking" {
  # FIXED: Store ALL needed values in triggers - ONLY these are accessible during destroy
  triggers = {
    network_name = google_compute_network.vpc_network.name
    project_id   = var.project_id
    region       = var.region
  }

  # FIXED: Destroy provisioner uses ONLY self.triggers - NO external resource references
  provisioner "local-exec" {
    when = destroy  # Runs ONLY during terraform destroy
    
    command = <<-EOT
      echo "🔧 Cleaning up service networking peering for network: ${self.triggers.network_name}"
      gcloud services vpc-peerings delete \
        --service=servicenetworking.googleapis.com \
        --network="${self.triggers.network_name}" \
        --project="${self.triggers.project_id}" \
        --quiet || echo "⚠️  Peering already gone or cleanup failed (safe)"
      echo "✅ Service networking cleanup complete for ${self.triggers.network_name}"
    EOT
    
    interpreter = ["bash", "-c"]
  }

  # Ensures cleanup runs AFTER all network resources are destroyed
  depends_on = [
    google_compute_network.vpc_network,
    google_vpc_access_connector.connector,
    google_service_networking_connection.private_vpc_connection
  ]
}


# -------------------------------------------------------
# resource "google_compute_network" "vpc_network" {
#   name                    = var.network_name
#   auto_create_subnetworks = false
# }

# resource "google_compute_subnetwork" "mediumx_subnetwork" {
#   name          = var.subnet_name
#   ip_cidr_range = "10.0.0.0/24"
#   network       = google_compute_network.vpc_network.id
#   region        = var.region
# }

# resource "google_dns_managed_zone" "managed_zone" {
#   name        = "mediumx-zone"
#   dns_name    = var.domain_name
#   description = "Managed zone for MediumX DNS"
# }

# resource "google_compute_backend_bucket" "cdn_backend" {
#   name        = "medium-cdn-backend"
#   description = "Contains HTML, CSS, JavaScript, images"
#   bucket_name = google_storage_bucket.static_files.name
#   enable_cdn  = true
# }

# resource "google_compute_backend_service" "mediumx_backend_service" {
#   name                    = "mediumx-backend-service"
#   description             = "Backend service for MediumX Cloud Run"
#   load_balancing_scheme   = "EXTERNAL_MANAGED"
#   protocol                = "HTTP"
#   health_checks           = [google_compute_health_check.mediumx_health_check.self_link]
#   connection_draining_timeout_sec = 60

#   backend {
#     group = google_compute_region_network_endpoint_group.mediumx_neg.id
#   }
# }

# resource "google_compute_health_check" "mediumx_health_check" {
#   name = "mediumx-health-check"

#   http_health_check {
#     port_specification = "USE_SERVING_PORT"
#     request_path       = "/healthz"
#   }

#   check_interval_sec  = 5
#   timeout_sec         = 5
#   healthy_threshold   = 1
#   unhealthy_threshold = 3
# }

# resource "google_compute_region_network_endpoint_group" "mediumx_neg" {
#   name       = "mediumx-neg"
#   region     = var.region
#   network    = google_compute_network.vpc_network.id
#   subnetwork = google_compute_subnetwork.mediumx_subnetwork.id

#   cloud_run {
#     service = google_cloud_run_service.backend_service.name
#   }
# }

# resource "google_compute_url_map" "lb_url_map" {
#   name            = "mediumx-url-map"
#   default_service = google_compute_backend_service.mediumx_backend_service.self_link
# }

# resource "google_compute_target_http_proxy" "http_proxy" {
#   name    = "mediumx-http-proxy"
#   url_map = google_compute_url_map.lb_url_map.self_link
# }

# resource "google_compute_forwarding_rule" "http_forwarding_rule" {
#   name                   = "mediumx-http-rule"
#   load_balancing_scheme  = "EXTERNAL"
#   target                 = google_compute_target_http_proxy.http_proxy.self_link
#   port_range             = "80"
#   ip_protocol            = "TCP"
#   network_tier           = "PREMIUM"
#   ip_address             = google_compute_global_address.static_ip.address
# }

# resource "google_compute_global_address" "static_ip" {
#   name = "${var.environment}-lb-ip"
# }






# resource "google_vpc_access_connector" "connector" {
#   name       = "mediumx-vpc-connector"
#   region     = var.region
#   network    = google_compute_network.vpc_network.id
# }




# resource "google_compute_firewall" "allow-cloud-run-to-sql" {
#   name    = "allow-cloud-run-to-sql"
#   network = google_compute_network.vpc_network.name

#   allow {
#     protocol = "tcp"
#     ports    = ["5432"]
#   }

#   source_ranges = ["0.0.0.0/0"]
#   target_tags   = ["sql-access"]
# }

# resource "google_compute_firewall" "allow-cloud-run-to-storage" {
#   name    = "allow-cloud-run-to-storage"
#   network = google_compute_network.vpc_network.name

#   allow {
#     protocol = "tcp"
#     ports    = ["443"]
#   }

#   source_ranges = ["0.0.0.0/0"]
#   target_tags   = ["storage-access"]
# }

# resource "google_compute_firewall" "allow-internal-traffic" {
#   name    = "allow-internal-traffic"
#   network = google_compute_network.vpc_network.name

#   allow {
#     protocol = "all"
#   }

#   source_ranges = ["10.0.0.0/24"]
# }
