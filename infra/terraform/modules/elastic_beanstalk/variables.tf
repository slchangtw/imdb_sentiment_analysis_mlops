variable "instance_type" {
  type        = string
  description = "EC2 instance type"
  default     = "t2.micro"
}

variable "max_instance_count" {
  type        = number
  description = "Max instance count in auto scaling group"
  default     = 2
}