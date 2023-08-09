# IMDB Sentiment Analysis

# ML Experimenting with mlflow

Start mlflow server on AWS
```bash
terraform init
terraform apply ｀-var-file="secrets.tfvars" --auto-approve
```

```bash
# Set mlflow tracking uri as environment variable
export MLFLOW_TRACKING_URI=$(terraform output -raw mlflow_tracking_uri)

# Run the command, and copy the result to a text file for later use
terraform output mlflow_command
```

Login to the EC2 instance and start the mlflow server.
```bash
pip install mlflow boto3 psycopg2-binary

# Start the mlflow server by the command copied from the previous step
```