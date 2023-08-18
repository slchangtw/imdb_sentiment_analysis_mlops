output "mlflow_tracking_uri" {
  description = "Mlflow tracking uri"
  value       = module.mlflow.mlflow_tracking_uri
}

output "mlflow_command" {
  description = "Command to start mlflow server"
  value       = module.mlflow.mlflow_command
  sensitive   = true
}

output "eb_web_service_url" {
  description = "Elastic Beanstalk web service url"
  value       = module.elastic_beanstalk.endpoint_url
}


