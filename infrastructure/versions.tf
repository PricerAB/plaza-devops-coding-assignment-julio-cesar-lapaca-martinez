terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.85.0"
    }
  }

  required_version = ">= 0.14"

  backend "gcs" {
    bucket = "code-assignment-terraform-state"
    prefix = "plaza-devops/terraform/state"
  }
}