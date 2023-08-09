output "mlflow_tracking_uri" {
  description = "Mlflow tracking uri"
  value       = module.mlflow.mlflow_tracking_uri
}

output "mlflow_command" {
  description = "Command to start mlflow server"
  value       = module.mlflow.mlflow_command
  sensitive   = true
}


