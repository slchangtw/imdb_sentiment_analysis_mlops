variable "imdb_reviews_bucket_name" {
  description = "Name of Bucket to store IMDB reviews"
  type        = string
  default     = "imdb-reviews-bucket"
}

variable "monitoring_bucket_name" {
  description = "Nane of Bucket to store monitoring data"
  type        = string
  default     = "imdb-reviews-monitoring-bucket"
}