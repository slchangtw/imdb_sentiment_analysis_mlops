output "endpoint_url" {
    description = "Endpoint url for the Elastic Beanstalk environment"
    value       = aws_elastic_beanstalk_environment.eb_env.endpoint_url
}