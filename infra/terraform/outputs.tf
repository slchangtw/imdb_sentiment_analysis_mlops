output "server_public_ip" {
  description = "Public IP address of the mlflow server"
  value       = aws_instance.mlflow_server.public_ip
}

output "database_endpoint" {
  description = "Database endpoint"
  value       = aws_db_instance.mlflow_db.endpoint
}