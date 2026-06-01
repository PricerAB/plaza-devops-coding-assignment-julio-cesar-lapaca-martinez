module "webapp" {
  source  = "../modules/helm_webapp"

  namespace = var.namespace
  helm_release_name = var.helm_release_name
  image_repository = var.image_repository
  image_tag = var.image_tag
  hello_world_message = "Hello World!"
}
