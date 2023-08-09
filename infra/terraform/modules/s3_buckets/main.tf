resource "aws_s3_bucket" "imdb_reviews_bucket" {
  bucket = var.bucket_name
}