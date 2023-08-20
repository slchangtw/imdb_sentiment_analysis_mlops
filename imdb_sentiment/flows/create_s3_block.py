from prefect_aws import AwsCredentials, S3Bucket

from imdb_sentiment.config import settings


def create_aws_creds_block():
    aws_creds_block = AwsCredentials(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    aws_creds_block.save(name="aws-credentials", overwrite=True)


def create_s3_bucket_block():
    aws_creds_block = AwsCredentials.load("aws-credentials")
    s3_bucket_block = S3Bucket(
        bucket_name="imdb-reviews-monitoring-bucket", credentials=aws_creds_block
    )
    s3_bucket_block.save(name="aws-s3", overwrite=True)


if __name__ == "__main__":
    create_aws_creds_block()
    create_s3_bucket_block()
