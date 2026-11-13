import os
import boto3


# load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()


s3_key = "data/premier_league_stats.csv"
bucket_name = os.getenv("s3_bucket_name")

def upload(file_path):
    """
    Uploads a file to an S3 bucket.

    :param file_path: Path to the file to upload
    """
    # Create an AWS Session
    aws_session = boto3.Session(profile_name=os.getenv("aws_profile"))

    # Create an S3 client
    s3_client = aws_session.client("s3")

    # Upload file to S3 Bucket
    with open(file_path, "rb") as file_data:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_key,
            Body=file_data
        )
