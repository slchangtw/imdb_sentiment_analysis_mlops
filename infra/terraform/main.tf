terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.9.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

module "mlflow" {
  source      = "./modules/mlflow"
  db_username = var.db_username
  db_password = var.db_password
}

module "s3_buckets" {
  source = "./modules/s3_buckets"
}

module "elastic_beanstalk" {
  source = "./modules/elastic_beanstalk"
}