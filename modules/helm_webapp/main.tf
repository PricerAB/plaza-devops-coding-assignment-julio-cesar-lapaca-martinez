resource "helm_release" "webapp" {
  name             = var.helm_release_name
  chart            = "${path.module}/../../helm-chart/webapp"
  namespace        = var.namespace
  create_namespace = true

  set {
    name  = "image.repository"
    value = var.image_repository
  }

  set {
    name  = "image.tag"
    value = var.image_tag
  }

  set {
    name  = "helloWorldMessage"
    value = var.hello_world_message
  }
}
