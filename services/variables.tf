variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
  default     = "default"
}

variable "helm_release_name" {
  description = "Helm release name"
  type        = string
  default     = "webapp"
}

variable "image_repository" {
  description = "Docker image repository"
  type        = string
  default     = "europe-north1-docker.pkg.dev/code-assignment-10/code-assignment-docker/webapp-candidateName"
}

variable "image_tag" {
  description = "Docker image tag"
  type        = string
  default     = "latest"
}
