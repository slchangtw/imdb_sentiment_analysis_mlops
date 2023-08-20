resource "aws_s3_bucket" "imdb_reviews_bucket" {
  bucket = var.imdb_reviews_bucket_name
}

resource "aws_s3_bucket" "imdb_reviews_monitoring_bucket" {
  bucket = var.monitoring_bucket_name
}
