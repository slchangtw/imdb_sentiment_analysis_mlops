# IMDB Sentiment Analysis

# ML Experimenting with mlflow

Start mlflow server on AWS
```bash
terraform init
terraform apply -var-file="secrets.tfvars" --auto-approve
```

Login to the EC2 instance and start the mlflow server.
```bash
pip install mlflow boto3 psycopg2-binary

mlflow server -h 0.0.0.0 -p 5000 \
    --backend-store-uri postgresql://<DB USERNAME>:<DB PASSWORD>@$<RDS ENDPOINT>/<DB NAME> \
    --default-artifact-root s3://<S3 ARTIFACT BUCKET>
```