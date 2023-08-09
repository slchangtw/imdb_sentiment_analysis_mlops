output "mlflow_tracking_uri" {
  description = "Mlflow tracking uri"
  value       = "http://${aws_eip.mlflow_eip.public_ip}:5000"
}

output "mlflow_command" {
  description = "Command to launch Mlflow server"
  value       = "mlflow server -h 0.0.0.0 -p 5000 --backend-store-uri postgresql://${var.db_username}:${var.db_password}@${aws_db_instance.mlflow_db.endpoint}/${var.settings.database.db_name} --default-artifact-root s3://${var.settings.artifact_bucket.name}"
  sensitive   = true
}