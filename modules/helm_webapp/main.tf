resource "helm_release" "webapp" {
  name             = "webapp"
  create_namespace = true

  # Use local path to chart

  # Use the variable namespace for the release
  
  # Set the chart values by reading variables input from services/variables.tf
}
