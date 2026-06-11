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
}

variable "image_tag" {
  description = "Docker image tag"
  type        = string
  default     = "latest"
}

variable "hello_world_message" {
  description = "Configurable message for the root endpoint"
  type        = string
  default     = "Hello, World!"
}
