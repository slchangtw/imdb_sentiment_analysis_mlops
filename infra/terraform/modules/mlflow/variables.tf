variable "vpc_cidr_block" {
  description = "CIDR block for vpc"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_count" {
  description = "Number of subnets"
  type        = map(number)
  default = {
    private = 2
  }

}

variable "settings" {
  description = "Configuration settings"
  type        = map(any)
  default = {
    "database" = {
      engine              = "postgres"
      engine_version      = "15.3"
      instance_class      = "db.t3.micro"
      db_name             = "mlflow"
      allocated_storage   = 10
      skip_final_snapshot = true
    },
    "mlflow_server" = {
      ami           = "ami-0dc7fe3dd38437495"
      instance_type = "t2.micro"
    },
    "artifact_bucket" = {
      name = "mlflow-artifact-remote-bucket"
    }
  }
}

variable "public_subnets_cidr_blocks" {
  description = "CIDR blocks for public subnets"
  type        = string
  default     = "10.0.1.0/24"
}


variable "private_subnets_cidr_blocks" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24"]
}

variable "db_username" {
  description = "Database username"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
