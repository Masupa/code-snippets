import io
import os
import boto3
import requests

from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

SEASON = "2627"
FILE_NAME = "EPL_" + SEASON + ".csv"
EPL_URL = f"https://football-data.co.uk/mmz4281/{SEASON}/E0.csv"


def create_aws_client():
    """Create and return an AWS S3 client using the configured profile."""
    # Create an AWS Session
    aws_session = boto3.Session(profile_name=os.getenv("AWS_PROFILE"))
    return aws_session.client("s3")


def extract_load(s3_client):
    """Download Premier League CSV data and upload it to the configured S3 bucket.

    Args:
        s3_client: AWS S3 client to use for uploading the data.

    Returns:
        None.

    Raises:
        Exception: If the response is not successful or the S3 bucket does not exist.
        requests.RequestException: If the HTTP request fails.
    """
    # Fetch Premier League data for the specified season from the URL
    response = requests.get(EPL_URL)

    if response.status_code == 200:
        # Store the response content in a BytesIO object for further processing
        data = io.BytesIO(response.content)

        try:
            # Upload the data to S3
            s3_client.put_object(
                Body=data,
                Bucket=os.environ.get("S3_BUCKET"),
                Key=f"{os.environ.get('BUCKET_PREFIX')}/{FILE_NAME}"
            )
        except s3_client.exceptions.NoSuchBucket:
            raise Exception(f"Bucket {os.environ.get('S3_BUCKET')} does not exist.")
        else:
            print(f"Successfully uploaded {FILE_NAME} to S3.")

            # Return a success response with status code and message
            return {
                'status_code': response.status_code,
                'message': f"Successfully uploaded {FILE_NAME} to S3."
            }
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")
