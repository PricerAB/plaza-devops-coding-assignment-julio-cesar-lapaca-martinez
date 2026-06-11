resource "helm_release" "webapp" {
  name             = var.helm_release_name
  chart            = "${path.module}/../../helm-chart/webapp"
  namespace        = var.namespace
  create_namespace = true

  values = [
    yamlencode({
      image = {
        repository = var.image_repository
        tag        = var.image_tag
      }
      helloWorldMessage = var.hello_world_message
    })
  ]
}
